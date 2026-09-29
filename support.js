"use strict";

const SUPPORT_ORDERS_KEY = "morrow.orders.v1";

function supportEscape(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function supportCurrency(value) {
  return new Intl.NumberFormat("zh-CN", {
    style: "currency",
    currency: "CNY",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(Number(value || 0));
}

function supportOrders() {
  try {
    const orders = JSON.parse(window.localStorage.getItem(SUPPORT_ORDERS_KEY) || "[]");
    return Array.isArray(orders) ? orders : [];
  } catch {
    return [];
  }
}

function supportOrderSummary(order) {
  const itemCount = (order.items || []).reduce(
    (sum, item) => sum + Number(item.quantity || 0),
    0,
  );
  return `订单号 ${order.orderNumber}，共 ${itemCount} 件商品，金额 ${supportCurrency(order.total)}，当前状态：${order.paymentStatus || "演示支付已确认"}。`;
}

function supportReply(message) {
  const text = String(message || "").trim();
  const lowered = text.toLowerCase();
  const orders = supportOrders();
  const orderCode = text.match(/MR[-\w]+/i)?.[0];

  if (/^(你好|您好|hi|hello|在吗)/i.test(text)) {
    return "你好，我可以帮你查最近订单、订单号、配送时间、退换货和保修。你直接说问题就可以。";
  }

  if (orderCode) {
    const matched = orders.find(
      (order) =>
        String(order.orderNumber || "").toLowerCase() === orderCode.toLowerCase(),
    );
    return matched
      ? supportOrderSummary(matched)
      : `当前浏览器没有找到 ${orderCode}。你可以打开“我的”页面查看本机订单；如果订单保存在演示服务端，也可以在那里按订单号查询。`;
  }

  if (/(订单|买了什么|购买记录|订单号|查单)/.test(text)) {
    if (orders.length === 0) {
      return "当前浏览器还没有保存订单。完成一次结账后，“我的”页面会自动显示订单号、商品、金额和状态。";
    }
    return `最近共有 ${orders.length} 笔订单。最新一笔：${supportOrderSummary(orders[0])} 打开“我的”页面可以看到全部订单。`;
  }

  if (/(发货|物流|配送|多久到|几天到|快递)/.test(text)) {
    return "现货商品预计 48 小时内出库。标准配送约 2 至 4 日；加急配送额外收取 ¥39，满 ¥999 免基础运费。演示订单不会产生真实物流。";
  }

  if (/(退货|退换|退款|换货|七天|30天)/.test(text)) {
    return "签收后 30 天内可以申请退换。商品、配件和原包装需要保持完整；人为损坏或缺少配件会影响处理结果。退款会按原支付入口返回，演示环境不会产生真实退款。";
  }

  if (/(保修|质保|维修|坏了|故障|售后)/.test(text)) {
    return "默认提供 2 年演示质保。请准备订单号、故障描述和商品照片；复杂维修会先检测，再确认维修、换货或退款方案。";
  }

  if (/(支付|扣款|支付宝|微信|银行卡|安全)/.test(text)) {
    return "银行卡、支付宝和微信支付都只是入口演示，不会采集真实支付信息，也不会真实扣款。订单状态只用于展示电子商务流程。";
  }

  if (/(地址|改地址|修改收货|收件人)/.test(text)) {
    return "订单尚未发货时可以申请修改地址。请把订单号和新地址一起发给售后支持；演示系统不会执行真实配送。";
  }

  if (/(发票|开票)/.test(text)) {
    return "演示环境不生成真实发票。正式商城通常会根据订单号和抬头信息开具电子发票，订单完成后可在订单详情中申请。";
  }

  if (/(人工|电话|客服|联系|投诉)/.test(text)) {
    return "复杂问题可以留下订单号和问题描述，由人工售后继续处理。演示服务时间为工作日 09:00 - 18:00。";
  }

  if (/(配置|内存|硬盘|容量|颜色|版本)/.test(text)) {
    return "商品详情页可以切换内存、硬盘、容量和颜色，价格会随配置实时变化。加入购物袋和订单里也会保留你选择的版本。";
  }

  if (/(谢谢|感谢|知道了|明白)/.test(text)) {
    return "不客气。需要查订单时，直接发订单号给我，例如 MR-20260928-ABC12。";
  }

  return "我目前可以回答订单查询、发货时间、退换货、保修、支付说明、修改地址和发票等常见问题。你也可以直接发送订单号。";
}

function installSupportWidget() {
  if (document.querySelector("[data-support-widget]")) return;

  const widget = document.createElement("section");
  widget.className = "support-widget";
  widget.dataset.supportWidget = "";
  widget.innerHTML = `
    <button
      class="support-trigger"
      type="button"
      data-support-trigger
      aria-label="打开虚拟客服"
      aria-expanded="false"
    >
      <i data-lucide="message-circle" aria-hidden="true"></i>
      <span>在线客服</span>
    </button>
    <div class="support-panel" data-support-panel hidden>
      <div class="support-head">
        <div>
          <p class="eyebrow">VIRTUAL SUPPORT</p>
          <h2>MORROW 客服</h2>
        </div>
        <button class="icon-button" type="button" data-support-close aria-label="关闭虚拟客服">
          <i data-lucide="x" aria-hidden="true"></i>
        </button>
      </div>
      <div class="support-messages" data-support-messages aria-live="polite"></div>
      <div class="support-quick-actions" aria-label="常见问题">
        <button type="button" data-support-question="查最近订单">查最近订单</button>
        <button type="button" data-support-question="多久发货">多久发货</button>
        <button type="button" data-support-question="如何退换">如何退换</button>
        <button type="button" data-support-question="保修多久">保修多久</button>
      </div>
      <form class="support-form" data-support-form>
        <label>
          <span class="sr-only">输入问题</span>
          <input
            type="text"
            name="message"
            placeholder="输入订单号或售后问题"
            autocomplete="off"
            maxlength="120"
          />
        </label>
        <button class="button button-primary" type="submit" aria-label="发送问题">
          <i data-lucide="send" aria-hidden="true"></i>
        </button>
      </form>
      <p class="support-note">虚拟客服用于演示，不连接真实人工客服或支付系统。</p>
    </div>
  `;
  document.body.append(widget);

  const panel = widget.querySelector("[data-support-panel]");
  const trigger = widget.querySelector("[data-support-trigger]");
  const messages = widget.querySelector("[data-support-messages]");
  const form = widget.querySelector("[data-support-form]");
  const input = form.elements.message;

  function refreshSupportIcons() {
    window.lucide?.createIcons({ attrs: { "aria-hidden": "true" } });
  }

  function addMessage(role, text) {
    const message = document.createElement("div");
    message.className = `support-message is-${role}`;
    message.innerHTML = `<p>${supportEscape(text)}</p>`;
    messages.append(message);
    messages.scrollTop = messages.scrollHeight;
  }

  function openSupport() {
    panel.hidden = false;
    trigger.setAttribute("aria-expanded", "true");
    if (!messages.children.length) {
      addMessage(
        "bot",
        "你好，我是虚拟客服。我可以帮你看最近订单、订单号、配送、退换和保修。",
      );
    }
    window.setTimeout(() => input.focus(), 80);
  }

  function closeSupport() {
    panel.hidden = true;
    trigger.setAttribute("aria-expanded", "false");
  }

  function sendQuestion(question) {
    const text = String(question || "").trim();
    if (!text) return;
    addMessage("user", text);
    addMessage("bot", supportReply(text));
    input.value = "";
  }

  trigger.addEventListener("click", () => {
    if (panel.hidden) openSupport();
    else closeSupport();
  });
  widget.querySelector("[data-support-close]").addEventListener("click", closeSupport);
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    sendQuestion(input.value);
  });
  widget.querySelectorAll("[data-support-question]").forEach((button) => {
    button.addEventListener("click", () => sendQuestion(button.dataset.supportQuestion));
  });
  document.addEventListener("click", (event) => {
    if (event.target.closest('[data-action="open-support"]')) openSupport();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !panel.hidden) closeSupport();
  });

  refreshSupportIcons();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", installSupportWidget, { once: true });
} else {
  installSupportWidget();
}
