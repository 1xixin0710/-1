"use strict";

const adminState = {
  code: window.sessionStorage.getItem("morrow.admin.code") || "",
  summary: null,
  products: [],
  orders: [],
  activeTab: "products",
  productQuery: "",
  staticMode: false,
};

const LOCAL_ORDERS_KEY = "morrow.orders.v1";
const LOCAL_INVENTORY_KEY = "morrow.admin.inventory.v1";

const adminDom = {
  login: document.querySelector("#admin-login"),
  console: document.querySelector("#admin-console"),
  loginForm: document.querySelector("[data-admin-login]"),
  logout: document.querySelector("[data-admin-logout]"),
  kpis: document.querySelector("#admin-kpis"),
  productRows: document.querySelector("#admin-product-rows"),
  orderRows: document.querySelector("#admin-order-rows"),
  productSearch: document.querySelector("[data-admin-product-search]"),
  reset: document.querySelector("[data-admin-reset]"),
  toast: document.querySelector("#admin-toast"),
};

const orderStatuses = {
  paid_demo: "演示支付已确认",
  processing: "处理中",
  shipped: "已发货",
  completed: "已完成",
  cancelled: "已取消",
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatCurrency(value) {
  return new Intl.NumberFormat("zh-CN", {
    style: "currency",
    currency: "CNY",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(Number(value || 0));
}

function formatDate(value) {
  return new Intl.DateTimeFormat("zh-CN", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function refreshIcons() {
  if (window.lucide) {
    window.lucide.createIcons({ attrs: { "aria-hidden": "true" } });
  }
}

function showAdminToast(title, message, isError = false) {
  const toast = document.createElement("div");
  toast.className = `toast${isError ? " is-error" : ""}`;
  toast.innerHTML = `
    <i data-lucide="${isError ? "circle-alert" : "circle-check"}" aria-hidden="true"></i>
    <div>
      <strong>${escapeHtml(title)}</strong>
      <span>${escapeHtml(message)}</span>
    </div>
  `;
  adminDom.toast.append(toast);
  refreshIcons();
  window.setTimeout(() => {
    toast.classList.add("is-leaving");
    window.setTimeout(() => toast.remove(), 190);
  }, 3200);
}

async function adminRequest(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      "X-Admin-Code": adminState.code,
      ...(options.headers || {}),
    },
  });
  const text = await response.text();
  let payload = {};
  try {
    payload = text ? JSON.parse(text) : {};
  } catch {
    payload = {};
  }
  if (!response.ok) {
    const error = new Error(payload.error?.message || "管理请求失败");
    error.status = response.status;
    throw error;
  }
  return payload;
}

function getLocalInventory() {
  try {
    const inventory = JSON.parse(
      window.localStorage.getItem(LOCAL_INVENTORY_KEY) || "{}",
    );
    return inventory && typeof inventory === "object" ? inventory : {};
  } catch {
    return {};
  }
}

function getLocalOrders() {
  try {
    const orders = JSON.parse(window.localStorage.getItem(LOCAL_ORDERS_KEY) || "[]");
    return Array.isArray(orders) ? orders : [];
  } catch {
    return [];
  }
}

function normalizeLocalOrder(order) {
  const checkout = order.checkout || {};
  return {
    ...order,
    status: order.status || "paid_demo",
    paymentStatus: order.paymentStatus || "演示支付已确认",
    paymentMethod: order.paymentMethod || checkout.paymentMethod || "card",
    customer: order.customer || {
      name: checkout.name || "本地演示客户",
      email: checkout.email || "",
      phone: checkout.phone || "",
    },
    delivery: order.delivery || {
      province: checkout.province || "",
      city: checkout.city || "",
      address: checkout.address || "",
      postalCode: checkout.postalCode || "",
      method: checkout.deliveryMethod || "standard",
    },
  };
}

function buildStaticSummary(products, orders) {
  const inventoryUnits = products.reduce(
    (sum, product) => sum + Number(product.stock || 0),
    0,
  );
  return {
    products: products.length,
    orders: orders.length,
    revenue: orders
      .filter((order) => order.status !== "cancelled")
      .reduce((sum, order) => sum + Number(order.total || 0), 0),
    inventoryUnits,
    lowStock: products.filter((product) => Number(product.stock) <= 8).length,
  };
}

function loadStaticAdminData() {
  const inventory = getLocalInventory();
  const catalog = Array.isArray(window.MORROW_PRODUCTS) ? window.MORROW_PRODUCTS : [];
  adminState.products = catalog.map((product) => ({
    ...product,
    ...(inventory[product.id] || {}),
  }));
  adminState.orders = getLocalOrders().map(normalizeLocalOrder);
  adminState.summary = buildStaticSummary(adminState.products, adminState.orders);
  adminState.staticMode = true;
}

function saveStaticProduct(productId, changes) {
  const inventory = getLocalInventory();
  inventory[productId] = {
    ...(inventory[productId] || {}),
    ...changes,
  };
  window.localStorage.setItem(LOCAL_INVENTORY_KEY, JSON.stringify(inventory));
}

function saveStaticOrder(orderNumber, status) {
  const orders = getLocalOrders();
  const nextOrders = orders.map((order) =>
    order.orderNumber === orderNumber ? { ...order, status } : order,
  );
  window.localStorage.setItem(LOCAL_ORDERS_KEY, JSON.stringify(nextOrders));
}

function resetStaticData() {
  window.localStorage.removeItem(LOCAL_INVENTORY_KEY);
  window.localStorage.setItem(LOCAL_ORDERS_KEY, "[]");
}

function renderKpis() {
  const summary = adminState.summary;
  const metrics = [
    { label: "商品总数", value: summary.products, icon: "package" },
    { label: "订单总数", value: summary.orders, icon: "receipt-text" },
    { label: "演示成交额", value: formatCurrency(summary.revenue), icon: "landmark" },
    { label: "库存件数", value: summary.inventoryUnits, icon: "boxes" },
    { label: "低库存预警", value: summary.lowStock, icon: "triangle-alert" },
  ];
  adminDom.kpis.innerHTML = metrics
    .map(
      (metric) => `
        <article class="admin-kpi">
          <i data-lucide="${metric.icon}" aria-hidden="true"></i>
          <span>${escapeHtml(metric.label)}</span>
          <strong>${escapeHtml(metric.value)}</strong>
        </article>
      `,
    )
    .join("");
}

function renderProducts() {
  const query = adminState.productQuery.trim().toLowerCase();
  const products = adminState.products.filter((product) =>
    [product.name, product.brand, product.categoryLabel]
      .join(" ")
      .toLowerCase()
      .includes(query),
  );

  if (products.length === 0) {
    adminDom.productRows.innerHTML = `
      <tr><td colspan="6" class="table-empty">没有匹配的商品</td></tr>
    `;
    return;
  }

  adminDom.productRows.innerHTML = products
    .map(
      (product) => `
        <tr data-product-row="${escapeHtml(product.id)}">
          <td>
            <div class="admin-product-cell">
              <img src="${escapeHtml(product.image)}" alt="" width="1200" height="1500" />
              <div>
                <strong>${escapeHtml(product.name)}</strong>
                <span>${escapeHtml(product.brand)}</span>
              </div>
            </div>
          </td>
          <td>${escapeHtml(product.categoryLabel)}</td>
          <td>
            <label class="inline-number">
              <span>¥</span>
              <input type="number" min="1" step="1" value="${Number(product.price)}" data-product-price />
            </label>
          </td>
          <td>
            <input class="stock-input" type="number" min="0" step="1" value="${Number(product.stock)}" data-product-stock />
          </td>
          <td>
            <select data-product-status>
              <option value="active" ${product.status === "active" ? "selected" : ""}>上架</option>
              <option value="hidden" ${product.status === "hidden" ? "selected" : ""}>隐藏</option>
            </select>
          </td>
          <td>
            <button class="table-action" type="button" data-save-product="${escapeHtml(product.id)}">
              保存
              <i data-lucide="save" aria-hidden="true"></i>
            </button>
          </td>
        </tr>
      `,
    )
    .join("");
  refreshIcons();
}

function renderOrders() {
  if (adminState.orders.length === 0) {
    adminDom.orderRows.innerHTML = `
      <tr>
        <td colspan="6" class="table-empty">
          暂无演示订单。返回商城完成一次结账后，订单会出现在这里。
        </td>
      </tr>
    `;
    return;
  }

  adminDom.orderRows.innerHTML = adminState.orders
    .map(
      (order) => `
        <tr data-order-row="${escapeHtml(order.orderNumber)}">
          <td>
            <strong>${escapeHtml(order.orderNumber)}</strong>
            <span class="table-subline">${formatDate(order.createdAt)}</span>
          </td>
          <td>
            <strong>${escapeHtml(order.customer.name)}</strong>
            <span class="table-subline">${escapeHtml(order.customer.email)}</span>
          </td>
          <td>
            <strong>${order.items.length} 种 / ${order.items.reduce((sum, item) => sum + item.quantity, 0)} 件</strong>
            <span class="table-subline">${escapeHtml(
              order.items
                .map((item) =>
                  item.variantLabel
                    ? `${item.name}（${item.variantLabel}）`
                    : item.name,
                )
                .join("、"),
            )}</span>
          </td>
          <td><strong>${formatCurrency(order.total)}</strong></td>
          <td>
            <select data-order-status>
              ${Object.entries(orderStatuses)
                .map(
                  ([value, label]) => `
                    <option value="${value}" ${order.status === value ? "selected" : ""}>
                      ${escapeHtml(label)}
                    </option>
                  `,
                )
                .join("")}
            </select>
          </td>
          <td>
            <button class="table-action" type="button" data-save-order="${escapeHtml(order.orderNumber)}">
              更新
              <i data-lucide="refresh-cw" aria-hidden="true"></i>
            </button>
          </td>
        </tr>
      `,
    )
    .join("");
  refreshIcons();
}

async function loadAdminData() {
  try {
    const payload = await adminRequest("./api/admin/summary");
    adminState.summary = payload.summary;
    adminState.products = payload.products || [];
    adminState.orders = payload.orders || [];
    adminState.staticMode = false;
  } catch (error) {
    if (adminState.code !== "2026") throw error;
    loadStaticAdminData();
  }
  const demoPill = document.querySelector(".admin-heading .demo-pill");
  if (demoPill) {
    demoPill.textContent = adminState.staticMode
      ? "GitHub Pages 本地演示模式"
      : "演示管理后台";
  }
  renderKpis();
  renderProducts();
  renderOrders();
}

function showConsole() {
  adminDom.login.hidden = true;
  adminDom.console.hidden = false;
  refreshIcons();
}

adminDom.loginForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  adminState.code = String(new FormData(adminDom.loginForm).get("code") || "").trim();
  try {
    await loadAdminData();
    window.sessionStorage.setItem("morrow.admin.code", adminState.code);
    showConsole();
    showAdminToast("已进入后台", "商品和订单数据已加载。");
  } catch (error) {
    showAdminToast("无法进入后台", error.message, true);
  }
});

adminDom.logout?.addEventListener("click", () => {
  window.sessionStorage.removeItem("morrow.admin.code");
  window.location.reload();
});

document.addEventListener("click", async (event) => {
  const tab = event.target.closest("[data-admin-tab]");
  if (tab) {
    adminState.activeTab = tab.dataset.adminTab;
    document.querySelectorAll("[data-admin-tab]").forEach((button) => {
      const active = button === tab;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-selected", String(active));
    });
    document.querySelectorAll("[data-admin-panel]").forEach((panel) => {
      panel.hidden = panel.dataset.adminPanel !== adminState.activeTab;
    });
    return;
  }

  const saveProduct = event.target.closest("[data-save-product]");
  if (saveProduct) {
    const row = saveProduct.closest("[data-product-row]");
    try {
      const changes = {
        price: Number(row.querySelector("[data-product-price]").value),
        stock: Number(row.querySelector("[data-product-stock]").value),
        status: row.querySelector("[data-product-status]").value,
      };
      if (adminState.staticMode) {
        saveStaticProduct(saveProduct.dataset.saveProduct, changes);
      } else {
        await adminRequest(
          `./api/admin/products/${encodeURIComponent(saveProduct.dataset.saveProduct)}`,
          {
            method: "PATCH",
            body: JSON.stringify(changes),
          },
        );
      }
      showAdminToast("商品已更新", "价格、库存和上下架状态已保存。");
      await loadAdminData();
    } catch (error) {
      showAdminToast("商品更新失败", error.message, true);
    }
    return;
  }

  const saveOrder = event.target.closest("[data-save-order]");
  if (saveOrder) {
    const row = saveOrder.closest("[data-order-row]");
    try {
      const status = row.querySelector("[data-order-status]").value;
      if (adminState.staticMode) {
        saveStaticOrder(saveOrder.dataset.saveOrder, status);
      } else {
        await adminRequest(
          `./api/admin/orders/${encodeURIComponent(saveOrder.dataset.saveOrder)}`,
          {
            method: "PATCH",
            body: JSON.stringify({ status }),
          },
        );
      }
      showAdminToast("订单已更新", "订单状态已同步到查询页。");
      await loadAdminData();
    } catch (error) {
      showAdminToast("订单更新失败", error.message, true);
    }
  }
});

adminDom.productSearch?.addEventListener("input", () => {
  adminState.productQuery = adminDom.productSearch.value;
  renderProducts();
});

adminDom.reset?.addEventListener("click", async () => {
  if (!window.confirm("重置全部演示订单和库存修改？")) return;
  try {
    if (adminState.staticMode) {
      resetStaticData();
    } else {
      await adminRequest("./api/admin/reset-demo", { method: "POST", body: "{}" });
    }
    showAdminToast("演示数据已重置", "订单已清空，库存和价格已恢复。");
    await loadAdminData();
  } catch (error) {
    showAdminToast("重置失败", error.message, true);
  }
});

if (adminState.code) {
  loadAdminData()
    .then(showConsole)
    .catch(() => {
      window.sessionStorage.removeItem("morrow.admin.code");
    });
} else {
  refreshIcons();
}
