"use strict";

const orderResults = document.querySelector("#order-results");
const lookupForm = document.querySelector("[data-order-lookup]");
const LOCAL_ORDERS_KEY = "morrow.orders.v1";

const statusLabels = {
  paid_demo: "演示支付已确认",
  processing: "处理中",
  shipped: "已发货",
  completed: "已完成",
  cancelled: "已取消",
};

const paymentLabels = {
  card: "银行卡",
  alipay: "支付宝",
  wechat: "微信支付",
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
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
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

function refreshIcons() {
  if (window.lucide) {
    window.lucide.createIcons({
      attrs: { "aria-hidden": "true" },
    });
  }
}

function renderEmpty(title, message, isError = false) {
  orderResults.innerHTML = `
    <div class="system-empty${isError ? " is-error" : ""}">
      <i data-lucide="${isError ? "circle-alert" : "package-search"}" aria-hidden="true"></i>
      <h2>${escapeHtml(title)}</h2>
      <p>${escapeHtml(message)}</p>
    </div>
  `;
  refreshIcons();
}

function renderOrders(orders, sourceLabel = "当前演示服务端") {
  if (orders.length === 0) {
    renderEmpty("没有找到订单", "请检查订单编号或邮箱是否正确。");
    return;
  }

  orderResults.innerHTML = `
    <div class="result-summary">
      <span>找到 <strong>${orders.length}</strong> 笔订单</span>
      <span>数据来自${escapeHtml(sourceLabel)}</span>
    </div>
    <div class="order-result-list">
      ${orders
        .map(
          (order) => `
            <article class="order-result-card">
              <div class="order-result-head">
                <div>
                  <p>${formatDate(order.createdAt)}</p>
                  <h2>${escapeHtml(order.orderNumber)}</h2>
                </div>
                <span class="status-chip status-${escapeHtml(order.status)}">
                  ${escapeHtml(statusLabels[order.status] || order.status)}
                </span>
              </div>
              <div class="order-result-meta">
                <div>
                  <span>收件人</span>
                  <strong>${escapeHtml(order.customer.name)}</strong>
                </div>
                <div>
                  <span>配送地址</span>
                  <strong>${escapeHtml(order.delivery.province)} ${escapeHtml(order.delivery.city)} ${escapeHtml(order.delivery.address)}</strong>
                </div>
                <div>
                  <span>支付入口</span>
                  <strong>${escapeHtml(paymentLabels[order.paymentMethod] || order.paymentMethod)} / ${escapeHtml(order.paymentStatus)}</strong>
                </div>
                <div>
                  <span>订单金额</span>
                  <strong>${formatCurrency(order.total)}</strong>
                </div>
              </div>
              <div class="order-result-items">
                ${order.items
                  .map(
                    (item) => `
                      <div class="order-result-item">
                        <img src="${escapeHtml(item.image)}" alt="" width="1200" height="1500" />
                        <div>
                          <strong>${escapeHtml(item.name)}</strong>
                          <span>${escapeHtml(item.variantLabel || item.color)} / 数量 ${item.quantity}</span>
                        </div>
                        <b>${formatCurrency(item.price * item.quantity)}</b>
                      </div>
                    `,
                  )
                  .join("")}
              </div>
              <div class="order-result-total">
                <span>商品 ${formatCurrency(order.subtotal)} / 配送 ${order.shipping === 0 ? "免费" : formatCurrency(order.shipping)} / 优惠 ${formatCurrency(order.discount)}</span>
                <strong>合计 ${formatCurrency(order.total)}</strong>
              </div>
            </article>
          `,
        )
        .join("")}
    </div>
  `;
  refreshIcons();
}

lookupForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const values = Object.fromEntries(new FormData(lookupForm).entries());
  const orderNumber = String(values.orderNumber || "").trim();
  const email = String(values.email || "").trim().toLowerCase();

  if (!orderNumber && !email) {
    renderEmpty("请先填写查询条件", "订单编号和邮箱至少填写一项。", true);
    return;
  }

  renderEmpty("正在查询", "正在读取服务端订单记录。");
  try {
    const params = new URLSearchParams();
    if (orderNumber) params.set("orderNumber", orderNumber);
    if (email) params.set("email", email);
    const response = await fetch(`./api/orders?${params.toString()}`);
    const payload = await response.json();
    if (!response.ok) {
      renderEmpty("查询失败", payload.error?.message || "服务端未返回订单。", true);
      return;
    }
    renderOrders(payload.orders || []);
  } catch {
    const orders = getLocalOrders()
      .map(normalizeLocalOrder)
      .filter((order) => {
        const matchesNumber = orderNumber && order.orderNumber === orderNumber;
        const matchesEmail =
          email && String(order.customer.email || "").toLowerCase() === email;
        return matchesNumber || matchesEmail;
      });
    renderOrders(orders, "浏览器本地演示数据");
  }
});

refreshIcons();
