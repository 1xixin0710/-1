"use strict";

const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const { URL } = require("node:url");

const ROOT = __dirname;
const DATA_DIR = path.join(ROOT, "data");
const CATALOG_PATH = path.join(DATA_DIR, "catalog.json");
const STATE_PATH = path.join(DATA_DIR, "store-state.json");
const PORT = Number(process.env.PORT || 4173);
const ADMIN_CODE = process.env.ADMIN_CODE || "2026";

const contentTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
};

function readJson(filePath, fallback) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return fallback;
  }
}

function writeJsonAtomic(filePath, value) {
  const temporaryPath = `${filePath}.tmp`;
  fs.writeFileSync(temporaryPath, JSON.stringify(value, null, 2), "utf8");
  fs.renameSync(temporaryPath, filePath);
}

function loadCatalog() {
  const catalog = readJson(CATALOG_PATH, []);
  if (!Array.isArray(catalog) || catalog.length === 0) {
    throw new Error("data/catalog.json is missing or empty");
  }
  return catalog;
}

function createInitialState(catalog) {
  return {
    meta: {
      storeName: "MORROW Market",
      createdAt: new Date().toISOString(),
      priceUpdatedAt: "2026-09-28",
      currency: "CNY",
      paymentMode: "demo",
    },
    inventory: Object.fromEntries(
      catalog.map((product) => [
        product.id,
        {
          stock: product.stock,
          price: product.price,
          status: "active",
        },
      ]),
    ),
    orders: [],
    audit: [],
  };
}

function loadState(catalog) {
  const existing = readJson(STATE_PATH, null);
  const state = existing || createInitialState(catalog);
  state.meta = { ...createInitialState(catalog).meta, ...(state.meta || {}) };
  state.inventory = state.inventory || {};
  state.orders = Array.isArray(state.orders) ? state.orders : [];
  state.audit = Array.isArray(state.audit) ? state.audit : [];

  catalog.forEach((product) => {
    state.inventory[product.id] = {
      stock: product.stock,
      price: product.price,
      status: "active",
      ...(state.inventory[product.id] || {}),
    };
  });

  writeJsonAtomic(STATE_PATH, state);
  return state;
}

const catalog = loadCatalog();
const state = loadState(catalog);

function getProducts() {
  return catalog.map((product) => {
    const inventory = state.inventory[product.id] || {};
    return {
      ...product,
      price: Number(inventory.price ?? product.price),
      stock: Number(inventory.stock ?? product.stock),
      status: inventory.status || "active",
    };
  });
}

function productById(id) {
  return getProducts().find((product) => product.id === id);
}

function variantGroups(product) {
  return Array.isArray(product?.variantGroups) ? product.variantGroups : [];
}

function normalizeVariantSelections(product, selections = {}) {
  return Object.fromEntries(
    variantGroups(product).map((group) => {
      const selected = group.options.find(
        (option) => option.id === selections[group.id],
      );
      const fallback = group.options.find(
        (option) => option.id === product.defaultVariant?.[group.id],
      );
      return [group.id, (selected || fallback || group.options[0]).id];
    }),
  );
}

function variantOption(product, groupId, optionId) {
  return variantGroups(product)
    .find((group) => group.id === groupId)
    ?.options.find((option) => option.id === optionId);
}

function variantPrice(product, selections = {}) {
  const normalized = normalizeVariantSelections(product, selections);
  const delta = variantGroups(product).reduce(
    (sum, group) =>
      sum +
      Number(variantOption(product, group.id, normalized[group.id])?.priceDelta || 0),
    0,
  );
  return Math.max(0, Number(product.price || 0) + delta);
}

function variantLabel(product, selections = {}) {
  const normalized = normalizeVariantSelections(product, selections);
  return variantGroups(product)
    .map((group) => variantOption(product, group.id, normalized[group.id])?.label)
    .filter(Boolean)
    .join(" / ");
}

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
  });
  response.end(JSON.stringify(payload));
}

function sendError(response, statusCode, message, details = undefined) {
  sendJson(response, statusCode, {
    error: {
      message,
      ...(details ? { details } : {}),
    },
  });
}

function readBody(request, limit = 1024 * 1024) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    request.on("data", (chunk) => {
      size += chunk.length;
      if (size > limit) {
        reject(new Error("Request body is too large"));
        request.destroy();
        return;
      }
      chunks.push(chunk);
    });
    request.on("end", () => {
      try {
        const raw = Buffer.concat(chunks).toString("utf8");
        resolve(raw ? JSON.parse(raw) : {});
      } catch {
        reject(new Error("Request body must be valid JSON"));
      }
    });
    request.on("error", reject);
  });
}

function authorizeAdmin(request, url) {
  const supplied =
    request.headers["x-admin-code"] ||
    url.searchParams.get("adminCode") ||
    "";
  return supplied === ADMIN_CODE;
}

function getPublicOrder(order) {
  return {
    orderNumber: order.orderNumber,
    createdAt: order.createdAt,
    status: order.status,
    paymentStatus: order.paymentStatus,
    customer: {
      name: order.customer.name,
      email: order.customer.email,
      phone: order.customer.phone,
    },
    delivery: {
      province: order.delivery.province,
      city: order.delivery.city,
      address: order.delivery.address,
      postalCode: order.delivery.postalCode,
      method: order.delivery.method,
    },
    items: order.items,
    subtotal: order.subtotal,
    shipping: order.shipping,
    discount: order.discount,
    total: order.total,
    paymentMethod: order.paymentMethod,
  };
}

function getSummary() {
  const products = getProducts();
  const paidOrders = state.orders.filter((order) => order.status !== "cancelled");
  const revenue = paidOrders.reduce((sum, order) => sum + Number(order.total || 0), 0);
  const inventoryUnits = products.reduce(
    (sum, product) => sum + Number(product.stock || 0),
    0,
  );
  const lowStock = products.filter((product) => product.stock <= 8).length;
  const orderStatusCounts = state.orders.reduce((result, order) => {
    result[order.status] = (result[order.status] || 0) + 1;
    return result;
  }, {});

  return {
    products: products.length,
    orders: state.orders.length,
    revenue,
    inventoryUnits,
    lowStock,
    orderStatusCounts,
    recentOrders: state.orders.slice(0, 8).map(getPublicOrder),
    lowStockProducts: products
      .filter((product) => product.stock <= 8)
      .sort((a, b) => a.stock - b.stock)
      .slice(0, 10)
      .map((product) => ({
        id: product.id,
        name: product.name,
        stock: product.stock,
        brand: product.brand,
      })),
  };
}

function createOrderNumber() {
  const date = new Date();
  const datePart = [
    date.getFullYear(),
    String(date.getMonth() + 1).padStart(2, "0"),
    String(date.getDate()).padStart(2, "0"),
  ].join("");
  const suffix = Math.random().toString(36).slice(2, 7).toUpperCase();
  return `MR${datePart}${suffix}`;
}

function validateOrderPayload(payload) {
  const errors = {};
  const allowedMethods = new Set(["card", "alipay", "wechat"]);
  const deliveryMethods = new Set(["standard", "express"]);
  const customer = payload.customer || {};
  const delivery = payload.delivery || {};
  const items = Array.isArray(payload.items) ? payload.items : [];

  if (!String(customer.name || "").trim()) errors.customerName = "请输入姓名";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(customer.email || ""))) {
    errors.customerEmail = "请输入有效邮箱";
  }
  if (!/^1[3-9]\d{9}$/.test(String(customer.phone || "").replace(/\s/g, ""))) {
    errors.customerPhone = "请输入有效手机号";
  }
  if (!String(delivery.province || "").trim()) errors.province = "请输入省份";
  if (!String(delivery.city || "").trim()) errors.city = "请输入城市";
  if (String(delivery.address || "").trim().length < 6) errors.address = "请输入完整地址";
  if (!/^\d{6}$/.test(String(delivery.postalCode || ""))) errors.postalCode = "请输入邮编";
  if (!deliveryMethods.has(payload.deliveryMethod)) errors.deliveryMethod = "配送方式无效";
  if (!allowedMethods.has(payload.paymentMethod)) errors.paymentMethod = "支付方式无效";
  if (items.length === 0) errors.items = "购物袋不能为空";

  items.forEach((item) => {
    const product = productById(item.productId);
    const quantity = Number(item.quantity);
    if (!product) errors.items = `商品不存在: ${item.productId}`;
    if (!Number.isInteger(quantity) || quantity < 1) {
      errors.items = `商品数量无效: ${item.productId}`;
    }
    if (product && quantity > product.stock) {
      errors.items = `${product.name} 库存不足`;
    }
  });

  return errors;
}

async function handleApi(request, response, url) {
  const pathname = url.pathname;

  if (request.method === "GET" && pathname === "/api/health") {
    sendJson(response, 200, {
      ok: true,
      service: "morrow-store",
      paymentMode: "demo",
      time: new Date().toISOString(),
    });
    return;
  }

  if (request.method === "GET" && pathname === "/api/products") {
    const query = String(url.searchParams.get("q") || "").toLowerCase();
    const category = String(url.searchParams.get("category") || "");
    const products = getProducts().filter((product) => {
      const matchesCategory = !category || category === "all" || product.category === category;
      const variantSearch = variantGroups(product)
        .flatMap((group) => [
          group.label,
          ...group.options.map((option) => option.label),
        ])
        .join(" ");
      const haystack = [
        product.name,
        product.displayName,
        product.brand,
        product.description,
        product.materials,
        variantSearch,
      ]
        .join(" ")
        .toLowerCase();
      return matchesCategory && (!query || haystack.includes(query));
    });
    sendJson(response, 200, {
      products,
      total: products.length,
      priceUpdatedAt: state.meta.priceUpdatedAt,
    });
    return;
  }

  const productMatch = pathname.match(/^\/api\/products\/([^/]+)$/);
  if (request.method === "GET" && productMatch) {
    const product = productById(decodeURIComponent(productMatch[1]));
    if (!product) {
      sendError(response, 404, "商品不存在");
      return;
    }
    sendJson(response, 200, { product });
    return;
  }

  if (request.method === "POST" && pathname === "/api/orders") {
    try {
      const payload = await readBody(request);
      const errors = validateOrderPayload(payload);
      if (Object.keys(errors).length > 0) {
        sendError(response, 422, "订单信息校验失败", errors);
        return;
      }

      const items = payload.items.map((item) => {
        const product = productById(item.productId);
        const variant = normalizeVariantSelections(product, item.variant || {});
        return {
          productId: product.id,
          name: product.displayName || product.name,
          brand: product.brand,
          color: String(item.color || product.colors?.[0]?.name || "默认"),
          variant,
          variantLabel: variantLabel(product, variant),
          quantity: Number(item.quantity),
          price: variantPrice(product, variant),
          image: product.image,
        };
      });
      const subtotal = items.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0,
      );
      const baseShipping = subtotal >= 999 ? 0 : 49;
      const expressFee = payload.deliveryMethod === "express" ? 39 : 0;
      const discount =
        String(payload.discountCode || "").toUpperCase() === "MORROW10"
          ? Math.round(subtotal * 0.1)
          : 0;
      const shipping = baseShipping + expressFee;

      const order = {
        orderNumber: createOrderNumber(),
        createdAt: new Date().toISOString(),
        status: "paid_demo",
        paymentStatus: "演示支付已确认",
        paymentMethod: payload.paymentMethod,
        customer: {
          name: String(payload.customer.name).trim(),
          email: String(payload.customer.email).trim().toLowerCase(),
          phone: String(payload.customer.phone).trim(),
        },
        delivery: {
          province: String(payload.delivery.province).trim(),
          city: String(payload.delivery.city).trim(),
          address: String(payload.delivery.address).trim(),
          postalCode: String(payload.delivery.postalCode).trim(),
          method: payload.deliveryMethod,
        },
        items,
        subtotal,
        shipping,
        discount,
        total: Math.max(0, subtotal + shipping - discount),
        note: String(payload.note || "").trim(),
      };

      items.forEach((item) => {
        const inventory = state.inventory[item.productId];
        inventory.stock = Math.max(0, Number(inventory.stock) - item.quantity);
      });
      state.orders.unshift(order);
      state.audit.unshift({
        type: "order.created",
        orderNumber: order.orderNumber,
        createdAt: order.createdAt,
      });
      writeJsonAtomic(STATE_PATH, state);
      sendJson(response, 201, { order: getPublicOrder(order) });
    } catch (error) {
      sendError(response, 400, error.message);
    }
    return;
  }

  if (request.method === "GET" && pathname === "/api/orders") {
    const orderNumber = String(url.searchParams.get("orderNumber") || "").trim();
    const email = String(url.searchParams.get("email") || "").trim().toLowerCase();
    if (!orderNumber && !email) {
      sendError(response, 400, "请提供订单编号或邮箱");
      return;
    }
    const orders = state.orders.filter((order) => {
      const matchesNumber = orderNumber && order.orderNumber === orderNumber;
      const matchesEmail = email && order.customer.email === email;
      return matchesNumber || matchesEmail;
    });
    sendJson(response, 200, { orders: orders.map(getPublicOrder) });
    return;
  }

  if (pathname.startsWith("/api/admin/")) {
    if (!authorizeAdmin(request, url)) {
      sendError(response, 401, "管理密钥无效");
      return;
    }

    if (request.method === "GET" && pathname === "/api/admin/summary") {
      sendJson(response, 200, {
        summary: getSummary(),
        products: getProducts(),
        orders: state.orders.slice(0, 100).map(getPublicOrder),
      });
      return;
    }

    const adminProductMatch = pathname.match(/^\/api\/admin\/products\/([^/]+)$/);
    if (request.method === "PATCH" && adminProductMatch) {
      const productId = decodeURIComponent(adminProductMatch[1]);
      const product = productById(productId);
      if (!product) {
        sendError(response, 404, "商品不存在");
        return;
      }
      try {
        const payload = await readBody(request);
        const inventory = state.inventory[productId];
        if (payload.price !== undefined) {
          const price = Number(payload.price);
          if (!Number.isFinite(price) || price <= 0) {
            sendError(response, 422, "价格必须大于 0");
            return;
          }
          inventory.price = Math.round(price);
        }
        if (payload.stock !== undefined) {
          const stock = Number(payload.stock);
          if (!Number.isInteger(stock) || stock < 0) {
            sendError(response, 422, "库存必须是非负整数");
            return;
          }
          inventory.stock = stock;
        }
        if (payload.status !== undefined) {
          if (!["active", "hidden"].includes(payload.status)) {
            sendError(response, 422, "商品状态无效");
            return;
          }
          inventory.status = payload.status;
        }
        state.audit.unshift({
          type: "product.updated",
          productId,
          changes: payload,
          createdAt: new Date().toISOString(),
        });
        writeJsonAtomic(STATE_PATH, state);
        sendJson(response, 200, { product: productById(productId) });
      } catch (error) {
        sendError(response, 400, error.message);
      }
      return;
    }

    const orderMatch = pathname.match(/^\/api\/admin\/orders\/([^/]+)$/);
    if (request.method === "PATCH" && orderMatch) {
      const order = state.orders.find(
        (item) => item.orderNumber === decodeURIComponent(orderMatch[1]),
      );
      if (!order) {
        sendError(response, 404, "订单不存在");
        return;
      }
      try {
        const payload = await readBody(request);
        const allowedStatuses = new Set([
          "paid_demo",
          "processing",
          "shipped",
          "completed",
          "cancelled",
        ]);
        if (!allowedStatuses.has(payload.status)) {
          sendError(response, 422, "订单状态无效");
          return;
        }
        order.status = payload.status;
        state.audit.unshift({
          type: "order.updated",
          orderNumber: order.orderNumber,
          status: payload.status,
          createdAt: new Date().toISOString(),
        });
        writeJsonAtomic(STATE_PATH, state);
        sendJson(response, 200, { order: getPublicOrder(order) });
      } catch (error) {
        sendError(response, 400, error.message);
      }
      return;
    }

    if (request.method === "POST" && pathname === "/api/admin/reset-demo") {
      state.orders = [];
      state.inventory = Object.fromEntries(
        catalog.map((product) => [
          product.id,
          { stock: product.stock, price: product.price, status: "active" },
        ]),
      );
      state.audit.unshift({
        type: "demo.reset",
        createdAt: new Date().toISOString(),
      });
      writeJsonAtomic(STATE_PATH, state);
      sendJson(response, 200, { ok: true, summary: getSummary() });
      return;
    }

    sendError(response, 404, "管理接口不存在");
    return;
  }

  sendError(response, 404, "API 接口不存在");
}

function serveStatic(response, pathname) {
  const requested =
    pathname === "/"
      ? "/index.html"
      : pathname.endsWith("/")
        ? `${pathname}index.html`
        : pathname;
  const normalized = path.normalize(decodeURIComponent(requested)).replace(/^(\.\.[/\\])+/, "");
  const filePath = path.join(ROOT, normalized);

  if (!filePath.startsWith(ROOT)) {
    sendError(response, 403, "禁止访问");
    return;
  }

  fs.stat(filePath, (error, stats) => {
    if (error || !stats.isFile()) {
      sendError(response, 404, "文件不存在");
      return;
    }
    const extension = path.extname(filePath).toLowerCase();
    response.writeHead(200, {
      "Content-Type": contentTypes[extension] || "application/octet-stream",
      "Cache-Control": extension === ".html" ? "no-cache" : "public, max-age=3600",
    });
    fs.createReadStream(filePath).pipe(response);
  });
}

const server = http.createServer(async (request, response) => {
  const url = new URL(request.url, `http://${request.headers.host || "localhost"}`);
  try {
    if (url.pathname.startsWith("/api/")) {
      await handleApi(request, response, url);
    } else if (request.method === "GET" || request.method === "HEAD") {
      serveStatic(response, url.pathname);
    } else {
      sendError(response, 405, "请求方法不允许");
    }
  } catch (error) {
    console.error(error);
    sendError(response, 500, "服务器内部错误");
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`MORROW Store running at http://127.0.0.1:${PORT}`);
  console.log(`Admin console: http://127.0.0.1:${PORT}/admin/`);
  console.log(`Demo admin code: ${ADMIN_CODE}`);
});
