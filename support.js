"use strict";

const SUPPORT_ORDERS_KEY = "morrow.orders.v1";
const SUPPORT_AI_ENDPOINT = "https://text.pollinations.ai/openai";
const SUPPORT_MAX_TURNS = 6;

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

function supportLocalReply(message) {
  const text = String(message || "").trim();
  const orders = supportOrders();
  const orderCode = text.match(/MR[-\w]+/i)?.[0];

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
    return "订单尚未发货时可以申请修改地址。请把订单号和新地址一起发给售后；演示系统不会执行真实配送。";
  }

  if (/(发票|开票)/.test(text)) {
    return "演示环境不生成真实发票。正式商城通常会根据订单号和抬头信息开具电子发票。";
  }

  return "";
}

function supportProducts() {
  const liveProducts = window.MORROW_STORE?.products?.();
  const products = Array.isArray(liveProducts)
    ? liveProducts
    : window.MORROW_PRODUCTS;
  return Array.isArray(products) ? products : [];
}

function supportCategoryIntent(text) {
  if (/(手机|拍照|影像|自拍|旗舰机)/.test(text)) return "phone";
  if (/(电脑|笔记本|办公本|游戏本|轻薄本)/.test(text)) return "computer";
  if (/(相机|微单|单反|摄影|镜头)/.test(text)) return "camera";
  if (/(耳机|音箱|音响|降噪|听歌)/.test(text)) return "audio";
  if (/(平板|上网课|手写)/.test(text)) return "tablet";
  if (/(键盘|鼠标|外设|桌面)/.test(text)) return "desk";
  if (/(家电|空调|洗衣机|净化器|扫地|清洁)/.test(text)) return "appliance";
  return null;
}

function supportRelevantProducts(text) {
  const products = supportProducts();
  const category = supportCategoryIntent(text);
  const budget = Number(
    text.match(/(?:预算|以内|不超过|低于|左右)?\s*(\d{3,6})\s*(?:元|块)?/)?.[1] || 0,
  );
  const lowered = text.toLowerCase();
  const brands = [...new Set(products.map((product) => String(product.brand || "")))]
    .filter((brand) => brand && lowered.includes(brand.toLowerCase()));

  const ranked = products
    .map((product) => {
      let score = Number(product.featured ? 3 : 0);
      if (category && product.category === category) score += 12;
      if (
        brands.some(
          (brand) => String(product.brand).toLowerCase() === brand.toLowerCase(),
        )
      ) {
        score += 9;
      }
      if (budget && Number(product.price) <= budget) score += 4;
      if (budget && Number(product.price) > budget * 1.15) score -= 8;
      const haystack =
        `${product.name} ${product.brand} ${product.categoryLabel}`.toLowerCase();
      if (
        lowered
          .split(/[^\p{L}\p{N}]+/u)
          .some((word) => word.length > 1 && haystack.includes(word))
      ) {
        score += 5;
      }
      score += Math.min(4, Math.log10(Number(product.sales || 1)));
      return { product, score };
    })
    .sort((a, b) => b.score - a.score);

  return ranked
    .filter((entry) => entry.score > 0)
    .slice(0, 8)
    .map((entry) => entry.product);
}

function supportProductContext(message) {
  return supportRelevantProducts(message)
    .map(
      (product) =>
        `- ${product.displayName || product.name}｜${supportCurrency(product.price)}｜${product.brand}｜${product.categoryLabel}｜评分 ${product.rating}｜${product.stock > 0 ? "有货" : "缺货"}`,
    )
    .join("\n");
}

async function supportAiReply(message, history) {
  const localReply = supportLocalReply(message);
  if (localReply) return localReply;

  const productContext = supportProductContext(message);
  const systemPrompt = [
    "你是 MORROW 生活集市的 AI 导购，用自然、克制的中文回答。",
    "优先根据下面提供的商品上下文推荐 2-3 件商品，说明价格、定位和适合人群。",
    "商品价格是公开参考价叠加实时行情演示，不能承诺最低价、库存或真实成交。",
    "不要编造上下文里没有的商品、优惠、物流或支付结果。",
    "订单、物流、退换、保修、支付、发票问题只按商城演示规则说明事实。",
    "回答控制在 180 个汉字左右，不使用 Markdown 表格。",
    "",
    "当前商品上下文：",
    productContext || "- 暂无匹配商品，请先追问预算和用途。",
  ].join("\n");

  const messages = [
    { role: "system", content: systemPrompt },
    ...history.slice(-SUPPORT_MAX_TURNS),
    { role: "user", content: message },
  ];

  const controller = new AbortController();
  const timeout = window.setTimeout(() => controller.abort(), 30000);
  try {
    const response = await fetch(SUPPORT_AI_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
      body: JSON.stringify({
        model: "openai-fast",
        messages,
        temperature: 0.55,
        max_tokens: 260,
        reasoning_effort: "low",
      }),
    });
    if (!response.ok) throw new Error(`AI ${response.status}`);
    const payload = await response.json();
    const reply = String(payload.choices?.[0]?.message?.content || "").trim();
    if (!reply) throw new Error("Empty AI reply");
    return reply.slice(0, 700);
  } catch {
    const products = supportProducts();
    const fallback = supportRelevantProducts(message)
      .slice(0, 3)
      .map(
        (product) =>
          `${product.displayName || product.name} ${supportCurrency(product.price)}`,
      )
      .join("、");
    return products.length
      ? `AI 响应暂时不稳定。可以先从这些同方向商品比较：${fallback}。你也可以补充预算、用途和偏好的品牌，我会继续帮你缩小范围。`
      : "AI 响应暂时不稳定。你可以先告诉我预算、用途和偏好的品牌，我会按商城现有商品继续筛选。";
  } finally {
    window.clearTimeout(timeout);
  }
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
      aria-label="打开 AI 导购"
      aria-expanded="false"
    >
      <i data-lucide="sparkles" aria-hidden="true"></i>
      <span>AI 导购</span>
    </button>
    <div class="support-panel" data-support-panel hidden>
      <div class="support-head">
        <div>
          <p class="eyebrow">AI SHOPPING CONCIERGE</p>
          <h2>MORROW AI 导购</h2>
          <span class="support-online"><i></i> 在线</span>
        </div>
        <button class="icon-button" type="button" data-support-close aria-label="关闭 AI 导购">
          <i data-lucide="x" aria-hidden="true"></i>
        </button>
      </div>
      <div class="support-messages" data-support-messages aria-live="polite"></div>
      <div class="support-quick-actions" aria-label="常见问题">
        <button type="button" data-support-question="5000 元内拍照手机怎么选">5000 元拍照手机</button>
        <button type="button" data-support-question="推荐一款适合通勤的降噪耳机">通勤降噪耳机</button>
        <button type="button" data-support-question="最近有什么优惠">最近优惠</button>
        <button type="button" data-support-question="查最近订单">查最近订单</button>
      </div>
      <form class="support-form" data-support-form>
        <label>
          <span class="sr-only">输入问题</span>
          <input
            type="text"
            name="message"
            placeholder="说预算、用途或想比较的商品"
            autocomplete="off"
            maxlength="180"
          />
        </label>
        <button class="button button-primary" type="submit" aria-label="发送问题">
          <i data-lucide="send" aria-hidden="true"></i>
        </button>
      </form>
      <p class="support-note">AI 生成内容仅供参考，订单与支付说明以页面展示为准。</p>
    </div>
  `;
  document.body.append(widget);

  const panel = widget.querySelector("[data-support-panel]");
  const trigger = widget.querySelector("[data-support-trigger]");
  const messages = widget.querySelector("[data-support-messages]");
  const form = widget.querySelector("[data-support-form]");
  const input = form.elements.message;
  const history = [];
  let isSending = false;

  function refreshSupportIcons() {
    window.lucide?.createIcons({ attrs: { "aria-hidden": "true" } });
  }

  function addMessage(role, text) {
    const message = document.createElement("div");
    message.className = `support-message is-${role}`;
    const paragraph = document.createElement("p");
    paragraph.textContent = text;
    message.append(paragraph);
    messages.append(message);
    messages.scrollTop = messages.scrollHeight;
    return message;
  }

  function addTyping() {
    const message = document.createElement("div");
    message.className = "support-message is-bot support-typing";
    message.innerHTML = "<p><i></i><i></i><i></i></p>";
    messages.append(message);
    messages.scrollTop = messages.scrollHeight;
    return message;
  }

  function openSupport() {
    panel.hidden = false;
    trigger.setAttribute("aria-expanded", "true");
    if (!messages.children.length) {
      addMessage(
        "bot",
        "你好，我是 MORROW AI 导购。告诉我预算、用途或想比较的商品，我会从当前商城里给你精简建议。",
      );
    }
    window.setTimeout(() => input.focus(), 80);
  }

  function closeSupport() {
    panel.hidden = true;
    trigger.setAttribute("aria-expanded", "false");
  }

  async function sendQuestion(question) {
    const text = String(question || "").trim();
    if (!text || isSending) return;
    isSending = true;
    addMessage("user", text);
    input.value = "";
    const typing = addTyping();
    const reply = await supportAiReply(text, history);
    typing.remove();
    addMessage("bot", reply);
    history.push(
      { role: "user", content: text },
      { role: "assistant", content: reply },
    );
    isSending = false;
    input.focus();
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
    button.addEventListener("click", () =>
      sendQuestion(button.dataset.supportQuestion),
    );
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
