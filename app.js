"use strict";

const STORAGE_KEYS = {
  cart: "morrow.cart.v1",
  orders: "morrow.orders.v1",
  discount: "morrow.discount.v1",
};

const legacyProducts = [
  {
    id: "aura-speaker",
    name: "AURA 01 织物便携音响",
    series: "SOUND / 001",
    category: "audio",
    price: 1299,
    compareAt: 1499,
    featured: true,
    stock: 12,
    description:
      "紧凑机身包覆耐磨织物，声音保持开阔，也保留足够清晰的低频。适合桌面、床头和短途出行。",
    materials: "再生聚酯织物、阳极氧化铝、硅胶防滑底",
    delivery: "现货商品将在 48 小时内发出，满 ¥999 免费配送。",
    image: "./assets/products/aura-speaker.jpg",
    colors: [
      { name: "深岩黑", value: "#17191d" },
      { name: "雾蓝", value: "#8095ae" },
    ],
  },
  {
    id: "halo-lamp",
    name: "HALO 01 可调光台灯",
    series: "LIGHT / 001",
    category: "light",
    price: 899,
    compareAt: 999,
    featured: true,
    stock: 8,
    description:
      "灯光可以向下聚焦阅读，也可以转向墙面制造柔和环境光。结构仅保留必要关节，调节顺手。",
    materials: "粉末喷涂钢、磨砂铝、暖白 LED 光源",
    delivery: "北京、上海、广州、深圳预计次日送达。",
    image: "./assets/products/halo-lamp.jpg",
    colors: [
      { name: "石墨灰", value: "#54595e" },
      { name: "柔白", value: "#e9e7e0" },
    ],
  },
  {
    id: "fold-headphones",
    name: "FOLD ANC 头戴耳机",
    series: "SOUND / 002",
    category: "audio",
    price: 1899,
    compareAt: null,
    featured: false,
    stock: 15,
    description:
      "为通勤和长时间聆听设计。头梁压力经过重新分配，降噪保持克制，不会产生明显耳压。",
    materials: "蛋白皮耳罩、再生 ABS、记忆棉",
    delivery: "全国大部分地区 2 至 3 日送达。",
    image: "./assets/products/fold-headphones.jpg",
    colors: [
      { name: "曜石黑", value: "#18191c" },
      { name: "砂岩灰", value: "#a5a3a0" },
    ],
  },
  {
    id: "frame-keyboard",
    name: "FRAME 70 无线键盘",
    series: "DESK / 002",
    category: "desk",
    price: 699,
    compareAt: 799,
    featured: false,
    stock: 18,
    description:
      "低键程与紧凑布局适合长时间输入。金属底板提供稳定支撑，同时保持桌面视觉轻盈。",
    materials: "阳极氧化铝、PBT 键帽、硅胶缓冲层",
    delivery: "下单后 48 小时内出库。",
    image: "./assets/products/frame-keyboard.jpg",
    colors: [
      { name: "银灰", value: "#c5c7ca" },
      { name: "深空灰", value: "#4d5157" },
    ],
  },
  {
    id: "drift-backpack",
    name: "DRIFT 18 城市背包",
    series: "TRAVEL / 003",
    category: "travel",
    price: 1180,
    compareAt: 1290,
    featured: false,
    stock: 5,
    description:
      "18L 容量覆盖日常通勤和短途出差。主仓开口清晰，电脑层与随身物品互不干扰。",
    materials: "再生尼龙、防泼水涂层、YKK 拉链",
    delivery: "大件包装将在 48 小时内发出。",
    image: "./assets/products/drift-backpack.jpg",
    colors: [
      { name: "深海蓝", value: "#1f3048" },
      { name: "煤黑", value: "#1a1c20" },
    ],
  },
  {
    id: "arc-watch",
    name: "ARC S 圆形智能腕表",
    series: "MOTION / 004",
    category: "objects",
    price: 1599,
    compareAt: 1799,
    featured: false,
    stock: 9,
    description:
      "以圆形表盘简化信息层级，只保留日常真正需要的提醒、运动和睡眠记录。",
    materials: "再生铝表壳、液态硅胶表带、矿物玻璃",
    delivery: "附赠长表带，预计 2 至 3 日送达。",
    image: "./assets/products/arc-watch.jpg",
    colors: [
      { name: "雾银", value: "#d8d9dc" },
      { name: "夜黑", value: "#22252a" },
    ],
  },
  {
    id: "form-chair",
    name: "FORM 01 模压餐椅",
    series: "OBJECT / 005",
    category: "objects",
    price: 1699,
    compareAt: null,
    featured: false,
    stock: 4,
    description:
      "一体成型座面提供稳定承托，细木腿让体量保持轻盈。适合餐桌、书桌和需要临时落座的角落。",
    materials: "回收聚丙烯座面、白蜡木椅腿、钢制连接件",
    delivery: "家具商品预计 5 至 7 日送达，部分地区提供入户配送。",
    image: "./assets/products/form-chair.jpg",
    colors: [
      { name: "乌木黑", value: "#242424" },
      { name: "苔藓绿", value: "#53665a" },
    ],
  },
  {
    id: "still-cup",
    name: "STILL 陶瓷杯",
    series: "OBJECT / 006",
    category: "objects",
    price: 239,
    compareAt: 269,
    featured: false,
    stock: 24,
    description:
      "扎实杯壁让饮品保持温度，宽把手适合完整掌握。适合咖啡、茶，也适合作为独立摆件。",
    materials: "高温炻瓷、哑光釉面",
    delivery: "现货商品将在 48 小时内发出。",
    image: "./assets/products/still-cup.jpg",
    colors: [
      { name: "月白", value: "#eeeDE8" },
      { name: "炭灰", value: "#777a7c" },
    ],
  },
];

const products = Array.isArray(window.MORROW_PRODUCTS)
  ? [...window.MORROW_PRODUCTS]
  : legacyProducts;

const state = {
  route: "store",
  category: "all",
  sort: "featured",
  search: "",
  selectedBrand: "all",
  priceBand: "all",
  inStockOnly: false,
  visibleCount: 16,
  catalogSource: "本地商品数据",
  priceUpdatedAt: "2026-09-28",
  activeProductId: null,
  selectedColors: {},
  selectedVariants: {},
  galleryIndex: 0,
  quantity: 1,
  cart: readStorage(STORAGE_KEYS.cart, []),
  orders: readStorage(STORAGE_KEYS.orders, []),
  discountApplied: readStorage(STORAGE_KEYS.discount, false),
  isLoadingCatalog: false,
  paymentStage: "idle",
  checkoutDraft: null,
  lastOrder: null,
  previousFocus: null,
};

const dom = {
  storeView: document.querySelector('[data-view="store"]'),
  productView: document.querySelector('[data-view="product"]'),
  checkoutView: document.querySelector('[data-view="checkout"]'),
  confirmationView: document.querySelector('[data-view="confirmation"]'),
  catalogGrid: document.querySelector("#catalog-grid"),
  cartDrawer: document.querySelector("[data-cart-drawer]"),
  cartContent: document.querySelector("[data-cart-content]"),
  cartFooter: document.querySelector("[data-cart-footer]"),
  cartCount: document.querySelector("[data-cart-count]"),
  drawerScrim: document.querySelector("[data-drawer-scrim]"),
  mobileMenu: document.querySelector("[data-mobile-menu]"),
  searchOverlay: document.querySelector("[data-search-overlay]"),
  searchInput: document.querySelector("[data-search-input]"),
  catalogMeta: document.querySelector("[data-catalog-meta]"),
  loadMoreButton: document.querySelector('[data-action="load-more"]'),
  brandFilter: document.querySelector("[data-brand-filter]"),
  priceFilter: document.querySelector("[data-price-filter]"),
  stockFilter: document.querySelector("[data-stock-filter]"),
  toastRegion: document.querySelector("#toast-region"),
};

function readStorage(key, fallback) {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function writeStorage(key, value) {
  try {
    window.localStorage.setItem(key, JSON.stringify(value));
  } catch {
    showToast("无法保存", "浏览器存储当前不可用，购物袋只会在本次访问中保留。", true);
  }
}

function productById(id) {
  return products.find((product) => product.id === id);
}

function variantGroups(product) {
  return Array.isArray(product?.variantGroups) ? product.variantGroups : [];
}

function defaultVariantSelections(product) {
  return Object.fromEntries(
    variantGroups(product).map((group) => {
      const preferred = group.options.find(
        (option) => option.id === product.defaultVariant?.[group.id],
      );
      return [group.id, (preferred || group.options[0]).id];
    }),
  );
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

function selectedVariants(product) {
  if (!product) return {};
  const selections = normalizeVariantSelections(
    product,
    state.selectedVariants[product.id] || defaultVariantSelections(product),
  );
  state.selectedVariants[product.id] = selections;
  return selections;
}

function variantOption(product, groupId, optionId) {
  return variantGroups(product)
    .find((group) => group.id === groupId)
    ?.options.find((option) => option.id === optionId);
}

function variantPrice(product, selections = selectedVariants(product)) {
  const normalized = normalizeVariantSelections(product, selections);
  const delta = variantGroups(product).reduce(
    (sum, group) => sum + Number(variantOption(product, group.id, normalized[group.id])?.priceDelta || 0),
    0,
  );
  return Math.max(0, Number(product.price || 0) + delta);
}

function variantCompareAt(product, selections = selectedVariants(product)) {
  if (!product.compareAt) return null;
  const normalized = normalizeVariantSelections(product, selections);
  const delta = variantGroups(product).reduce(
    (sum, group) => sum + Number(variantOption(product, group.id, normalized[group.id])?.priceDelta || 0),
    0,
  );
  return Math.max(0, Number(product.compareAt) + delta);
}

function variantSummary(product, selections = selectedVariants(product)) {
  const normalized = normalizeVariantSelections(product, selections);
  return variantGroups(product)
    .map((group) => variantOption(product, group.id, normalized[group.id])?.label)
    .filter(Boolean)
    .join(" / ");
}

function variantSignature(product, selections = selectedVariants(product)) {
  const normalized = normalizeVariantSelections(product, selections);
  return variantGroups(product)
    .map((group) => `${group.id}:${normalized[group.id]}`)
    .join("|");
}

function variantPriceRange(product) {
  let combinations = [0];
  variantGroups(product).forEach((group) => {
    combinations = combinations.flatMap((current) =>
      group.options.map((option) => current + Number(option.priceDelta || 0)),
    );
  });
  const minimum = Math.min(...combinations.map((delta) => product.price + delta));
  const maximum = Math.max(...combinations.map((delta) => product.price + delta));
  return { minimum, maximum };
}

function productDisplayName(product) {
  return product?.displayName || product?.name || "";
}

function productSearchText(product) {
  const variantLabels = variantGroups(product)
    .flatMap((group) => [group.label, ...group.options.map((option) => option.label)])
    .join(" ");
  return [
    product.name,
    product.displayName,
    product.brand,
    product.description,
    product.materials,
    variantLabels,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}

function formatCurrency(value) {
  return new Intl.NumberFormat("zh-CN", {
    style: "currency",
    currency: "CNY",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function refreshIcons() {
  if (window.lucide) {
    window.lucide.createIcons({
      attrs: {
        "aria-hidden": "true",
      },
    });
  }
}

function showToast(title, message, isError = false) {
  const toast = document.createElement("div");
  toast.className = `toast${isError ? " is-error" : ""}`;
  toast.innerHTML = `
    <i data-lucide="${isError ? "circle-alert" : "circle-check"}" aria-hidden="true"></i>
    <div>
      <strong>${escapeHtml(title)}</strong>
      <span>${escapeHtml(message)}</span>
    </div>
  `;
  dom.toastRegion.append(toast);
  refreshIcons();

  window.setTimeout(() => {
    toast.classList.add("is-leaving");
    window.setTimeout(() => toast.remove(), 190);
  }, 3300);
}

function getCartDetails() {
  return state.cart
    .map((item, cartIndex) => {
      const product = productById(item.productId);
      if (!product) return null;
      const variant = normalizeVariantSelections(product, item.variant || {});
      return {
        ...item,
        cartIndex,
        product,
        variant,
        variantKey: variantSignature(product, variant),
        variantLabel: variantSummary(product, variant),
        variantPrice: variantPrice(product, variant),
        variantCompareAt: variantCompareAt(product, variant),
      };
    })
    .filter(Boolean);
}

function cartCount() {
  return state.cart.reduce((count, item) => count + item.quantity, 0);
}

function getTotals() {
  const subtotal = getCartDetails().reduce(
    (sum, item) => sum + item.variantPrice * item.quantity,
    0,
  );
  const shipping = subtotal === 0 || subtotal >= 999 ? 0 : 49;
  const discount = state.discountApplied ? Math.round(subtotal * 0.1) : 0;
  return {
    subtotal,
    shipping,
    discount,
    total: Math.max(0, subtotal + shipping - discount),
  };
}

function persistCart() {
  writeStorage(STORAGE_KEYS.cart, state.cart);
  updateCartCount();
  renderCart();
}

function updateCartCount() {
  const count = cartCount();
  dom.cartCount.textContent = String(count);
  dom.cartCount.setAttribute("aria-hidden", count === 0 ? "true" : "false");
}

function addToCart(productId, color, quantity = 1, selections = undefined) {
  const product = productById(productId);
  if (!product || product.stock === 0) {
    showToast("暂时无法加入", "该商品当前没有可用库存。", true);
    return;
  }

  const variant = normalizeVariantSelections(
    product,
    selections || selectedVariants(product),
  );
  const selectedVariantKey = variantSignature(product, variant);
  const existing = state.cart.find(
    (item) =>
      item.productId === productId &&
      item.color === color &&
      variantSignature(product, item.variant || {}) === selectedVariantKey,
  );
  const currentQuantity = existing ? existing.quantity : 0;
  const nextQuantity = Math.min(product.stock, currentQuantity + quantity);

  if (existing) {
    existing.quantity = nextQuantity;
  } else {
    state.cart.push({ productId, color, variant, quantity: nextQuantity });
  }

  persistCart();
  openCart();
  showToast(
    "已加入购物袋",
    `${productDisplayName(product)} / ${variantSummary(product, variant)} / ${color}`,
  );
}

function setCartQuantity(cartIndex, quantity) {
  const item = state.cart[cartIndex];
  if (!item) return;
  const product = productById(item.productId);
  const nextQuantity = Math.max(1, Math.min(product?.stock || 1, quantity));
  item.quantity = nextQuantity;
  persistCart();
}

function removeCartItem(cartIndex) {
  const item = state.cart[cartIndex];
  if (!item) return;
  const product = productById(item.productId);
  state.cart.splice(cartIndex, 1);
  persistCart();
  showToast("已从购物袋移除", product?.name || "商品");
}

function matchesPriceBand(price, band) {
  if (band === "all") return true;
  const [minimum, maximum] = band.split("-").map(Number);
  return price >= minimum && price <= maximum;
}

function populateBrandFilter() {
  if (!dom.brandFilter) return;
  const currentValue = state.selectedBrand;
  const brands = [...new Set(products.map((product) => product.brand).filter(Boolean))]
    .sort((a, b) => a.localeCompare(b, "zh-CN"));
  dom.brandFilter.innerHTML = `
    <option value="all">全部品牌</option>
    ${brands.map((brand) => `<option value="${escapeHtml(brand)}">${escapeHtml(brand)}</option>`).join("")}
  `;
  dom.brandFilter.value = brands.includes(currentValue) ? currentValue : "all";
  state.selectedBrand = dom.brandFilter.value;
}

function getFilteredProducts() {
  const query = state.search.trim().toLocaleLowerCase("zh-CN");
  let filtered = products.filter((product) => {
    const matchesCategory =
      state.category === "all" || product.category === state.category;
    const matchesBrand =
      state.selectedBrand === "all" || product.brand === state.selectedBrand;
    const matchesPrice = matchesPriceBand(
      variantPriceRange(product).minimum,
      state.priceBand,
    );
    const matchesStock = !state.inStockOnly || product.stock > 0;
    const haystack = `${product.series} ${productSearchText(product)}`.toLocaleLowerCase(
      "zh-CN",
    );
    return (
      matchesCategory &&
      matchesBrand &&
      matchesPrice &&
      matchesStock &&
      (!query || haystack.includes(query))
    );
  });

  return filtered.sort((a, b) => {
    if (state.sort === "price-asc") {
      return variantPriceRange(a).minimum - variantPriceRange(b).minimum;
    }
    if (state.sort === "price-desc") {
      return variantPriceRange(b).maximum - variantPriceRange(a).maximum;
    }
    if (state.sort === "newest") return products.indexOf(b) - products.indexOf(a);
    return (
      Number(b.featured) - Number(a.featured) ||
      products.indexOf(a) - products.indexOf(b)
    );
  });
}

function renderCatalog(forceSkeleton = false) {
  if (!dom.catalogGrid) return;

  if (forceSkeleton || state.isLoadingCatalog) {
    dom.catalogGrid.innerHTML = Array.from({ length: 8 })
      .map(
        (_, index) => `
          <div class="skeleton-card${index === 0 ? " is-featured" : ""}" aria-hidden="true">
            <div class="skeleton-media"></div>
            <div class="skeleton-line"></div>
            <div class="skeleton-line is-short"></div>
          </div>
        `,
      )
      .join("");
    return;
  }

  const filtered = getFilteredProducts();
  const visible = filtered.slice(0, state.visibleCount);

  if (dom.catalogMeta) {
    dom.catalogMeta.innerHTML = `
      <span>共 <strong>${filtered.length}</strong> 件商品，当前显示 ${visible.length} 件</span>
      <span>${escapeHtml(state.catalogSource)} · 参考价更新 ${escapeHtml(state.priceUpdatedAt)}</span>
    `;
  }

  if (dom.loadMoreButton) {
    dom.loadMoreButton.hidden = visible.length >= filtered.length;
    dom.loadMoreButton.innerHTML = `
      加载更多商品
      <i data-lucide="arrow-down" aria-hidden="true"></i>
    `;
  }

  if (filtered.length === 0) {
    dom.catalogGrid.innerHTML = `
      <div class="catalog-empty">
        <div class="catalog-empty-inner">
          <i data-lucide="search-x" aria-hidden="true"></i>
          <h3>没有找到匹配的商品</h3>
          <p>换一个名称、品牌或价格区间试试。当前检索为“${escapeHtml(state.search || "全部商品")}”。</p>
          <button class="button button-secondary" type="button" data-action="reset-search">
            清除筛选
          </button>
        </div>
      </div>
    `;
    refreshIcons();
    return;
  }

  dom.catalogGrid.innerHTML = visible
    .map(
      (product) => {
        const priceRange = variantPriceRange(product);
        const hasVariantRange = priceRange.maximum > priceRange.minimum;
        return `
        <article class="product-card${product.featured ? " is-featured" : ""}">
          <div
            class="product-card-media"
            role="button"
            tabindex="0"
            data-product-open="${product.id}"
            aria-label="查看 ${escapeHtml(productDisplayName(product))}"
          >
            <img
              src="${product.image}"
              alt="${escapeHtml(productDisplayName(product))}"
              width="1200"
              height="1500"
              loading="lazy"
            />
            <span class="product-card-badge">${escapeHtml(product.brand)}</span>
            <button
              class="quick-add"
              type="button"
              data-add-quick="${product.id}"
              aria-label="把 ${escapeHtml(productDisplayName(product))} 加入购物袋"
              ${product.stock === 0 ? "disabled" : ""}
            >
              <i data-lucide="${product.stock === 0 ? "package-x" : "plus"}" aria-hidden="true"></i>
            </button>
          </div>
          <div class="product-card-content">
            <div>
              <p class="product-card-series">${escapeHtml(product.series)}</p>
              <h3>${escapeHtml(productDisplayName(product))}</h3>
              <p class="product-card-description">${escapeHtml(product.description)}</p>
              ${
                variantGroups(product).length
                  ? `<p class="product-card-variant-note">可选 ${variantGroups(product)
                      .map((group) => group.label)
                      .join(" / ")}</p>`
                  : ""
              }
              <span class="product-stock${product.stock <= 5 ? " is-low" : ""}">
                ${product.stock === 0 ? "暂时缺货" : product.stock <= 5 ? `仅剩 ${product.stock} 件` : `现货 ${product.stock} 件`}
              </span>
            </div>
            <div class="product-card-price">
              <span>${formatCurrency(priceRange.minimum)}${hasVariantRange ? " 起" : ""}</span>
            </div>
          </div>
        </article>
      `;
      },
    )
    .join("");

  refreshIcons();
}

async function loadProductsFromApi(silent = false) {
  try {
    const response = await fetch("./api/products", {
      headers: { Accept: "application/json" },
    });
    if (!response.ok) return;
    const payload = await response.json();
    if (!Array.isArray(payload.products) || payload.products.length === 0) return;

    products.splice(
      0,
      products.length,
      ...payload.products.filter((product) => product.status !== "hidden"),
    );
    state.catalogSource = "服务器库存接口";
    state.priceUpdatedAt = payload.priceUpdatedAt || state.priceUpdatedAt;
    populateBrandFilter();
    renderCatalog();
    renderCart();
    if (!silent) refreshIcons();
  } catch {
    state.catalogSource = "本地商品数据";
  }
}

function selectedColor(product) {
  return state.selectedColors[product.id] || product.colors[0].name;
}

function productColor(product, colorName = selectedColor(product)) {
  return product.colors.find((color) => color.name === colorName) || product.colors[0];
}

function colorGallery(product, colorName = selectedColor(product)) {
  const color = productColor(product, colorName);
  if (Array.isArray(color.gallery) && color.gallery.length) {
    return color.gallery;
  }
  return [
    {
      src: color.image || product.image,
      position: "50% 50%",
      scale: 1,
      fit: "cover",
      filter: color.filter || "none",
    },
  ];
}

function galleryImageStyle(item) {
  return [
    `object-position:${escapeHtml(item.position || "50% 50%")}`,
    `object-fit:${escapeHtml(item.fit || "cover")}`,
    `transform:scale(${Number(item.scale || 1)})`,
    item.filter ? `filter:${escapeHtml(item.filter)}` : "",
  ]
    .filter(Boolean)
    .join(";");
}

function renderProduct(productId, preserveQuantity = false) {
  const product = productById(productId);
  if (!product) {
    navigate("store");
    return;
  }

  if (state.activeProductId !== product.id) {
    state.galleryIndex = 0;
  }
  state.activeProductId = product.id;
  if (!preserveQuantity) state.quantity = 1;
  const selections = selectedVariants(product);
  const currentPrice = variantPrice(product, selections);
  const currentCompareAt = variantCompareAt(product, selections);
  const colorName = selectedColor(product);
  const gallery = colorGallery(product, colorName);
  const galleryIndex = Math.max(
    0,
    Math.min(Number(state.galleryIndex || 0), gallery.length - 1),
  );
  const activeGalleryItem = gallery[galleryIndex];
  const isPanorama = activeGalleryItem.fit === "contain";
  const colorOptions = product.colors
    .map(
      (color) => `
        <button
          class="color-option${color.name === colorName ? " is-active" : ""}"
          type="button"
          data-color-option="${escapeHtml(color.name)}"
          aria-pressed="${color.name === colorName}"
        >
          <span class="color-swatch" style="--swatch:${color.value}"></span>
          ${escapeHtml(color.name)}
        </button>
      `,
    )
    .join("");
  const variantOptions = variantGroups(product)
    .map(
      (group) => `
        <section class="option-section" aria-labelledby="variant-${escapeHtml(group.id)}">
          <div class="option-head">
            <strong id="variant-${escapeHtml(group.id)}">${escapeHtml(group.label)}</strong>
            <span>价格随配置实时更新</span>
          </div>
          <div class="variant-options">
            ${group.options
              .map((option) => {
                const isActive = selections[group.id] === option.id;
                const delta = Number(option.priceDelta || 0);
                const deltaLabel =
                  delta > 0
                    ? ` +${formatCurrency(delta)}`
                    : delta < 0
                      ? ` -${formatCurrency(Math.abs(delta))}`
                      : "";
                return `
                  <button
                    class="variant-option${isActive ? " is-active" : ""}"
                    type="button"
                    data-variant-group="${escapeHtml(group.id)}"
                    data-variant-option="${escapeHtml(option.id)}"
                    aria-pressed="${isActive}"
                  >
                    <strong>${escapeHtml(option.label)}</strong>
                    <span>${deltaLabel || "基础配置"}</span>
                  </button>
                `;
              })
              .join("")}
          </div>
        </section>
      `,
    )
    .join("");

  dom.productView.innerHTML = `
    <div class="page-topline">
      <button class="back-button" type="button" data-action="back-store">
        <i data-lucide="arrow-left" aria-hidden="true"></i>
        返回全部商品
      </button>
      <span class="page-kicker">${escapeHtml(product.series)}</span>
    </div>

    <div class="product-detail">
      <div class="product-gallery">
        <div class="gallery-thumbnails" aria-label="商品图片">
          ${gallery
            .map(
              (item, index) => `
                <button
                  class="gallery-thumb${index === galleryIndex ? " is-active" : ""}"
                  type="button"
                  data-gallery-thumb="${index}"
                  aria-label="查看第 ${index + 1} 张商品图片"
                  aria-pressed="${index === galleryIndex}"
                >
                  <img
                    src="${escapeHtml(item.src)}"
                    alt=""
                    width="1200"
                    height="1500"
                    style="${galleryImageStyle(item)}"
                  />
                </button>
              `,
            )
            .join("")}
        </div>
        <div class="gallery-main${isPanorama ? " is-panorama" : ""}">
          <img
            src="${escapeHtml(activeGalleryItem.src)}"
            alt="${escapeHtml(`${productDisplayName(product)}，${colorName}，商品图 ${galleryIndex + 1}`)}"
            width="1200"
            height="1500"
            style="${galleryImageStyle(activeGalleryItem)}"
          />
          <span class="gallery-counter">${galleryIndex + 1} / ${gallery.length}</span>
        </div>
      </div>

      <div class="product-info">
        <p class="series">${escapeHtml(product.series)}</p>
        <h1>${escapeHtml(productDisplayName(product))}</h1>
        ${
          variantGroups(product).length
            ? `<p class="selected-variant-summary">已选：${escapeHtml(variantSummary(product, selections))}</p>`
            : ""
        }
        <div class="product-rating">
          <span class="rating-stars" aria-label="评分 ${Number(product.rating || 4.7).toFixed(1)} 分">
            ${Array.from({ length: 5 })
              .map(() => '<i data-lucide="star" aria-hidden="true"></i>')
              .join("")}
          </span>
          <span>${Number(product.rating || 4.7).toFixed(1)} / ${Number(product.reviewCount || 0).toLocaleString("zh-CN")} 条榜单点评</span>
        </div>
        <div class="product-price-line">
          <span class="price">${formatCurrency(currentPrice)}</span>
          ${currentCompareAt ? `<del>${formatCurrency(currentCompareAt)}</del>` : ""}
        </div>
        <div class="price-basis">
          <i data-lucide="database" aria-hidden="true"></i>
          <span>
            参考价，更新于 ${escapeHtml(product.source?.updatedAt || state.priceUpdatedAt)}。
            <a href="${escapeHtml(product.source?.url || "#")}" target="_blank" rel="noopener noreferrer">
              查看公开来源
            </a>
          </span>
        </div>
        <p class="product-description">${escapeHtml(product.description)}</p>

        ${variantOptions}

        <section class="option-section" aria-labelledby="color-title">
          <div class="option-head">
            <strong id="color-title">颜色</strong>
            <span data-selected-color-label>${escapeHtml(colorName)}</span>
          </div>
          <div class="color-options">${colorOptions}</div>
        </section>

        <section class="option-section" aria-labelledby="quantity-title">
          <div class="option-head">
            <strong id="quantity-title">数量</strong>
            <span>每单最多 ${product.stock} 件</span>
          </div>
          <div class="purchase-row">
            <div class="quantity-stepper">
              <button
                type="button"
                data-qty-change="-1"
                aria-label="减少数量"
                ${state.quantity <= 1 ? "disabled" : ""}
              >
                <i data-lucide="minus" aria-hidden="true"></i>
              </button>
              <output data-product-quantity>${state.quantity}</output>
              <button
                type="button"
                data-qty-change="1"
                aria-label="增加数量"
                ${state.quantity >= product.stock ? "disabled" : ""}
              >
                <i data-lucide="plus" aria-hidden="true"></i>
              </button>
            </div>
            <button
              class="button button-primary"
              type="button"
              data-action="add-product"
              ${product.stock === 0 ? "disabled" : ""}
            >
              <i data-lucide="shopping-bag" aria-hidden="true"></i>
              加入购物袋
            </button>
          </div>
          ${
            product.stock <= 5
              ? `
                <p class="stock-warning">
                  <i data-lucide="circle-alert" aria-hidden="true"></i>
                  当前库存仅剩 ${product.stock} 件
                </p>
              `
              : ""
          }
        </section>

        <div class="delivery-panel">
          <div>
            <i data-lucide="truck" aria-hidden="true"></i>
            <span>${escapeHtml(product.delivery)}</span>
          </div>
          <div>
            <i data-lucide="rotate-ccw" aria-hidden="true"></i>
            <span>商品及包装保持完整，支持 30 天内退换。</span>
          </div>
          <div>
            <i data-lucide="shield-check" aria-hidden="true"></i>
            <span>提供 2 年有限质保和在线售后支持。</span>
          </div>
        </div>

        <details class="product-facts">
          <summary>材质与维护</summary>
          <p>${escapeHtml(product.materials)}。建议使用柔软干布清洁，避免长时间接触强溶剂或尖锐物。</p>
        </details>
        <details class="product-facts">
          <summary>包装与配送</summary>
          <p>使用可回收纸质缓冲材料。现货商品将在 48 小时内完成出库。</p>
        </details>
      </div>
    </div>
  `;

  refreshIcons();
}

function renderCart() {
  if (!dom.cartContent || !dom.cartFooter) return;
  const items = getCartDetails();
  updateCartCount();

  if (items.length === 0) {
    dom.cartContent.innerHTML = `
      <div class="cart-empty">
        <div class="cart-empty-inner">
          <span class="empty-icon">
            <i data-lucide="shopping-bag" aria-hidden="true"></i>
          </span>
          <h3>购物袋还是空的</h3>
          <p>浏览本期器物，把真正会用到的带回家。</p>
          <button class="button button-secondary" type="button" data-action="close-cart">
            继续选购
          </button>
        </div>
      </div>
    `;
    dom.cartFooter.innerHTML = "";
    refreshIcons();
    return;
  }

  dom.cartContent.innerHTML = `
    <div class="cart-items">
      ${items
        .map(
          (item) => `
            <article class="cart-item">
              <div class="cart-item-image">
                <img src="${item.product.image}" alt="" width="1200" height="1500" />
              </div>
              <div>
                <div class="cart-item-head">
                  <div>
                    <h3>${escapeHtml(productDisplayName(item.product))}</h3>
                    <p>${escapeHtml(item.variantLabel)} / ${escapeHtml(item.color)}</p>
                  </div>
                  <button
                    class="remove-item"
                    type="button"
                    data-cart-remove="${item.cartIndex}"
                    aria-label="移除 ${escapeHtml(item.product.name)}"
                  >
                    <i data-lucide="trash-2" aria-hidden="true"></i>
                  </button>
                </div>
                <div class="cart-item-bottom">
                  <div class="cart-quantity">
                    <button
                      type="button"
                      data-cart-qty="${item.cartIndex}"
                      data-qty="${item.quantity - 1}"
                      aria-label="减少数量"
                      ${item.quantity <= 1 ? "disabled" : ""}
                    >
                      <i data-lucide="minus" aria-hidden="true"></i>
                    </button>
                    <output>${item.quantity}</output>
                    <button
                      type="button"
                      data-cart-qty="${item.cartIndex}"
                      data-qty="${item.quantity + 1}"
                      aria-label="增加数量"
                      ${item.quantity >= item.product.stock ? "disabled" : ""}
                    >
                      <i data-lucide="plus" aria-hidden="true"></i>
                    </button>
                  </div>
                  <strong class="cart-item-price">
                    ${formatCurrency(item.variantPrice * item.quantity)}
                  </strong>
                </div>
              </div>
            </article>
          `,
        )
        .join("")}
    </div>
  `;

  const totals = getTotals();
  dom.cartFooter.innerHTML = `
    <div class="discount-row">
      <input
        type="text"
        data-discount-input
        placeholder="优惠码 MORROW10"
        aria-label="优惠码"
        value="${state.discountApplied ? "MORROW10" : ""}"
      />
      <button type="button" data-action="apply-discount">
        ${state.discountApplied ? "已应用" : "应用"}
      </button>
    </div>
    <div class="cart-lines">
      <div class="cart-line">
        <span>商品小计</span>
        <span>${formatCurrency(totals.subtotal)}</span>
      </div>
      <div class="cart-line">
        <span>配送</span>
        <span>${totals.shipping === 0 ? "免费" : formatCurrency(totals.shipping)}</span>
      </div>
      ${
        totals.discount > 0
          ? `
            <div class="cart-line">
              <span>优惠 MORROW10</span>
              <span>-${formatCurrency(totals.discount)}</span>
            </div>
          `
          : ""
      }
    </div>
    <div class="cart-total">
      <span>合计</span>
      <strong>${formatCurrency(totals.total)}</strong>
    </div>
    <button class="button button-primary button-block" type="button" data-action="checkout">
      前往结账
      <i data-lucide="arrow-right" aria-hidden="true"></i>
    </button>
  `;
  refreshIcons();
}

function openCart() {
  closeMobileMenu(false);
  closeSearch(false);
  state.previousFocus = document.activeElement;
  dom.cartDrawer.classList.add("is-open");
  dom.cartDrawer.setAttribute("aria-hidden", "false");
  dom.drawerScrim.hidden = false;
  document.body.classList.add("is-locked");
  renderCart();
  window.setTimeout(() => dom.cartDrawer.querySelector("button")?.focus(), 80);
}

function closeCart(returnFocus = true) {
  dom.cartDrawer.classList.remove("is-open");
  dom.cartDrawer.setAttribute("aria-hidden", "true");
  if (!dom.mobileMenu.classList.contains("is-open")) {
    dom.drawerScrim.hidden = true;
    document.body.classList.remove("is-locked");
  }
  if (returnFocus && state.previousFocus instanceof HTMLElement) {
    state.previousFocus.focus();
  }
}

function openMobileMenu() {
  closeCart(false);
  state.previousFocus = document.activeElement;
  dom.mobileMenu.classList.add("is-open");
  dom.mobileMenu.setAttribute("aria-hidden", "false");
  dom.drawerScrim.hidden = false;
  document.body.classList.add("is-locked");
  window.setTimeout(() => dom.mobileMenu.querySelector("button")?.focus(), 80);
}

function closeMobileMenu(returnFocus = true) {
  dom.mobileMenu.classList.remove("is-open");
  dom.mobileMenu.setAttribute("aria-hidden", "true");
  if (!dom.cartDrawer.classList.contains("is-open")) {
    dom.drawerScrim.hidden = true;
    document.body.classList.remove("is-locked");
  }
  if (returnFocus && state.previousFocus instanceof HTMLElement) {
    state.previousFocus.focus();
  }
}

function openSearch() {
  closeCart(false);
  closeMobileMenu(false);
  state.previousFocus = document.activeElement;
  dom.searchOverlay.hidden = false;
  document.body.classList.add("is-locked");
  window.setTimeout(() => dom.searchInput?.focus(), 60);
}

function closeSearch(returnFocus = true) {
  if (dom.searchOverlay.hidden) return;
  dom.searchOverlay.hidden = true;
  if (!dom.cartDrawer.classList.contains("is-open") && !dom.mobileMenu.classList.contains("is-open")) {
    document.body.classList.remove("is-locked");
  }
  if (returnFocus && state.previousFocus instanceof HTMLElement) {
    state.previousFocus.focus();
  }
}

function navigate(route, productId = null) {
  if (route === "product" && productId) {
    window.location.hash = `product=${encodeURIComponent(productId)}`;
    return;
  }
  window.location.hash = route;
}

function parseRoute() {
  const hash = window.location.hash.replace(/^#/, "");
  if (hash.startsWith("product=")) {
    state.route = "product";
    state.activeProductId = decodeURIComponent(hash.slice("product=".length));
    return;
  }
  if (hash === "checkout" && getCartDetails().length > 0) {
    state.route = "checkout";
    return;
  }
  if (hash === "confirmation" && (state.lastOrder || state.orders.length > 0)) {
    state.route = "confirmation";
    return;
  }
  state.route = "store";
  state.activeProductId = null;
  state.paymentStage = "idle";
}

function renderRoute() {
  parseRoute();

  dom.storeView.hidden = state.route !== "store";
  dom.productView.hidden = state.route !== "product";
  dom.checkoutView.hidden = state.route !== "checkout";
  dom.confirmationView.hidden = state.route !== "confirmation";

  if (state.route === "store") {
    renderCatalog();
  } else if (state.route === "product") {
    renderProduct(state.activeProductId);
  } else if (state.route === "checkout") {
    renderCheckout();
  } else if (state.route === "confirmation") {
    renderConfirmation();
  }

  closeCart(false);
  closeMobileMenu(false);
  closeSearch(false);
  window.scrollTo({ top: 0, behavior: "auto" });
  refreshIcons();
}

function scrollToSection(id) {
  if (state.route !== "store") {
    window.location.hash = "store";
    window.setTimeout(() => scrollToSection(id), 100);
    return;
  }
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderCheckout() {
  if (getCartDetails().length === 0) {
    navigate("store");
    showToast("购物袋为空", "先选择商品，再进入结账。", true);
    return;
  }

  const totals = getTotals();
  const items = getCartDetails();
  const draft = state.checkoutDraft || {};
  const deliveryMethod = draft.deliveryMethod || "standard";
  const paymentMethod = draft.paymentMethod || "card";
  const deliveryFee = deliveryMethod === "express" ? 39 : 0;
  const orderTotal = totals.total + deliveryFee;

  if (state.paymentStage === "processing") {
    dom.checkoutView.innerHTML = `
      <div class="page-topline">
        <span class="back-button">
          <i data-lucide="lock-keyhole" aria-hidden="true"></i>
          安全结账
        </span>
        <span class="page-kicker">支付入口 / 演示模式</span>
      </div>
      <div class="checkout-layout">
        <div class="payment-processing">
          <div>
            <span class="processing-mark">
              <i data-lucide="loader-circle" aria-hidden="true"></i>
            </span>
            <h2>正在连接演示支付入口</h2>
            <p>正在模拟订单确认，不会请求银行卡，也不会产生任何真实扣款。</p>
          </div>
        </div>
        <aside class="order-summary">
          <h2>订单摘要</h2>
          <div class="summary-lines">
            <div class="summary-line">
              <span>商品数量</span>
              <span>${cartCount()} 件</span>
            </div>
            <div class="summary-line">
              <span>支付方式</span>
              <span>${paymentLabel(paymentMethod)}</span>
            </div>
            <div class="summary-total">
              <span>应付</span>
              <strong>${formatCurrency(orderTotal)}</strong>
            </div>
          </div>
        </aside>
      </div>
    `;
    refreshIcons();
    return;
  }

  dom.checkoutView.innerHTML = `
    <div class="page-topline">
      <button class="back-button" type="button" data-action="back-store">
        <i data-lucide="arrow-left" aria-hidden="true"></i>
        继续选购
      </button>
      <span class="page-kicker">演示支付入口</span>
    </div>

    <div class="checkout-layout">
      <div>
        <div class="checkout-heading">
          <p class="eyebrow">CHECKOUT</p>
          <h1>完成你的订单</h1>
          <p>填写配送信息并选择支付入口。提交后会进入演示支付流程，不会产生真实扣款。</p>
        </div>

        <form class="checkout-form" data-checkout-form novalidate>
          <section class="form-section">
            <div class="form-section-head">
              <h2>联系信息</h2>
              <span>用于订单通知</span>
            </div>
            <div class="form-grid">
              <div class="field">
                <label for="checkout-name">姓名</label>
                <input id="checkout-name" name="name" value="${escapeHtml(draft.name || "")}" placeholder="请输入收件人姓名" autocomplete="name" />
                <span class="field-error" data-error-for="name"></span>
              </div>
              <div class="field">
                <label for="checkout-email">电子邮箱</label>
                <input id="checkout-email" name="email" type="email" value="${escapeHtml(draft.email || "")}" placeholder="name@example.com" autocomplete="email" />
                <span class="field-error" data-error-for="email"></span>
              </div>
              <div class="field">
                <label for="checkout-phone">手机号码</label>
                <input id="checkout-phone" name="phone" value="${escapeHtml(draft.phone || "")}" placeholder="11 位手机号码" autocomplete="tel" inputmode="tel" />
                <span class="field-error" data-error-for="phone"></span>
              </div>
            </div>
          </section>

          <section class="form-section">
            <div class="form-section-head">
              <h2>配送地址</h2>
              <span>当前支持中国大陆地区</span>
            </div>
            <div class="form-grid">
              <div class="field">
                <label for="checkout-province">省份</label>
                <input id="checkout-province" name="province" value="${escapeHtml(draft.province || "")}" placeholder="例如：浙江省" autocomplete="address-level1" />
                <span class="field-error" data-error-for="province"></span>
              </div>
              <div class="field">
                <label for="checkout-city">城市</label>
                <input id="checkout-city" name="city" value="${escapeHtml(draft.city || "")}" placeholder="例如：杭州市" autocomplete="address-level2" />
                <span class="field-error" data-error-for="city"></span>
              </div>
              <div class="field is-full">
                <label for="checkout-address">详细地址</label>
                <input id="checkout-address" name="address" value="${escapeHtml(draft.address || "")}" placeholder="街道、门牌号、小区和房间号" autocomplete="street-address" />
                <span class="field-error" data-error-for="address"></span>
              </div>
              <div class="field">
                <label for="checkout-postal">邮政编码</label>
                <input id="checkout-postal" name="postalCode" value="${escapeHtml(draft.postalCode || "")}" placeholder="6 位邮政编码" autocomplete="postal-code" inputmode="numeric" />
                <span class="field-error" data-error-for="postalCode"></span>
              </div>
            </div>
          </section>

          <section class="form-section">
            <div class="form-section-head">
              <h2>配送方式</h2>
              <span>预计 2 至 7 日送达</span>
            </div>
            <div class="delivery-options">
              <label class="choice-card${deliveryMethod === "standard" ? " is-selected" : ""}">
                <input type="radio" name="deliveryMethod" value="standard" ${deliveryMethod === "standard" ? "checked" : ""} />
                <span class="radio-mark"></span>
                <span>
                  <strong>标准配送</strong>
                  <p>预计 3 至 5 个工作日送达</p>
                </span>
                <span class="choice-card-price">免费</span>
              </label>
              <label class="choice-card${deliveryMethod === "express" ? " is-selected" : ""}">
                <input type="radio" name="deliveryMethod" value="express" ${deliveryMethod === "express" ? "checked" : ""} />
                <span class="radio-mark"></span>
                <span>
                  <strong>优先配送</strong>
                  <p>预计 1 至 2 个工作日送达</p>
                </span>
                <span class="choice-card-price">+¥39</span>
              </label>
            </div>
          </section>

          <section class="form-section">
            <div class="form-section-head">
              <h2>支付入口</h2>
              <span class="payment-heading">
                <i data-lucide="shield-check" aria-hidden="true"></i>
                安全演示
              </span>
            </div>
            <div class="demo-notice">
              <i data-lucide="info" aria-hidden="true"></i>
              <div>
                <strong>演示支付模式</strong>
                <p>这里只展示支付入口和交互流程。不会连接支付平台，不会收集卡号，也不会产生真实扣款。</p>
              </div>
            </div>
            <div class="payment-options">
              ${paymentChoice("card", "银行卡", "跳转至模拟银行卡收银台", "credit-card", paymentMethod)}
              ${paymentChoice("alipay", "支付宝", "打开模拟支付宝入口", "wallet-cards", paymentMethod)}
              ${paymentChoice("wechat", "微信支付", "打开模拟微信支付入口", "scan-line", paymentMethod)}
            </div>
          </section>

          <div class="checkout-submit">
            <button class="button button-primary button-block" type="submit">
              前往支付
              <i data-lucide="arrow-right" aria-hidden="true"></i>
            </button>
            <p class="form-footnote">提交订单即表示已阅读演示支付说明，本流程不会产生真实交易。</p>
          </div>
        </form>
      </div>

      <aside class="order-summary">
        <h2>订单摘要</h2>
        <div class="summary-items">
          ${items
            .map(
              (item) => `
                <div class="summary-item">
                  <div class="summary-item-image">
                    <img src="${item.product.image}" alt="" width="1200" height="1500" />
                  </div>
                  <div>
                    <h3>${escapeHtml(productDisplayName(item.product))}</h3>
                    <p>${escapeHtml(item.variantLabel)} / ${escapeHtml(item.color)} / 数量 ${item.quantity}</p>
                  </div>
                  <strong>${formatCurrency(item.variantPrice * item.quantity)}</strong>
                </div>
              `,
            )
            .join("")}
        </div>
        <div class="summary-lines">
          <div class="summary-line">
            <span>商品小计</span>
            <span>${formatCurrency(totals.subtotal)}</span>
          </div>
          <div class="summary-line">
            <span>基础配送</span>
            <span>${totals.shipping === 0 ? "免费" : formatCurrency(totals.shipping)}</span>
          </div>
          ${
            totals.discount > 0
              ? `
                <div class="summary-line">
                  <span>优惠 MORROW10</span>
                  <span>-${formatCurrency(totals.discount)}</span>
                </div>
              `
              : ""
          }
          ${
            deliveryFee > 0
              ? `
                <div class="summary-line">
                  <span>优先配送</span>
                  <span>${formatCurrency(deliveryFee)}</span>
                </div>
              `
              : ""
          }
          <div class="summary-total">
            <span>应付</span>
            <strong>${formatCurrency(orderTotal)}</strong>
          </div>
        </div>
        <div class="secure-note">
          <i data-lucide="lock-keyhole" aria-hidden="true"></i>
          <span>支付说明仅用于前端演示。刷新页面后，商品会继续保留在购物袋中。</span>
        </div>
      </aside>
    </div>
  `;

  refreshIcons();
}

function paymentChoice(value, title, description, icon, selected) {
  return `
    <label class="choice-card${selected === value ? " is-selected" : ""}">
      <input type="radio" name="paymentMethod" value="${value}" ${selected === value ? "checked" : ""} />
      <span class="radio-mark"></span>
      <span>
        <strong>${title}</strong>
        <p>${description}</p>
      </span>
      <i data-lucide="${icon}" class="choice-card-price" aria-hidden="true"></i>
    </label>
  `;
}

function paymentLabel(value) {
  if (value === "alipay") return "支付宝";
  if (value === "wechat") return "微信支付";
  return "银行卡";
}

function validateCheckout(form) {
  const formData = new FormData(form);
  const values = Object.fromEntries(formData.entries());
  const errors = {};

  if (!String(values.name || "").trim()) errors.name = "请输入收件人姓名。";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(values.email || ""))) {
    errors.email = "请输入有效的电子邮箱。";
  }
  if (!/^1[3-9]\d{9}$/.test(String(values.phone || "").replace(/\s/g, ""))) {
    errors.phone = "请输入有效的 11 位手机号码。";
  }
  if (!String(values.province || "").trim()) errors.province = "请输入省份。";
  if (!String(values.city || "").trim()) errors.city = "请输入城市。";
  if (String(values.address || "").trim().length < 6) {
    errors.address = "请填写完整地址，至少包含 6 个字符。";
  }
  if (!/^\d{6}$/.test(String(values.postalCode || ""))) {
    errors.postalCode = "请输入 6 位邮政编码。";
  }

  form.querySelectorAll(".field").forEach((field) => {
    field.classList.remove("has-error");
  });
  form.querySelectorAll("[data-error-for]").forEach((errorNode) => {
    errorNode.textContent = "";
  });

  Object.entries(errors).forEach(([fieldName, message]) => {
    const input = form.elements[fieldName];
    const field = input?.closest(".field");
    const errorNode = form.querySelector(`[data-error-for="${fieldName}"]`);
    field?.classList.add("has-error");
    if (errorNode) errorNode.textContent = message;
  });

  if (Object.keys(errors).length > 0) {
    const firstInvalid = form.querySelector(".field.has-error input, .field.has-error textarea");
    firstInvalid?.focus();
    return null;
  }

  return {
    ...values,
    deliveryMethod: values.deliveryMethod || "standard",
    paymentMethod: values.paymentMethod || "card",
  };
}

async function completeOrder(checkout) {
  const cartItems = getCartDetails();
  const items = cartItems.map((item) => ({
    productId: item.product.id,
    name: productDisplayName(item.product),
    brand: item.product.brand,
    color: item.color,
    variant: item.variant,
    variantLabel: item.variantLabel,
    quantity: item.quantity,
    price: item.variantPrice,
    image: item.product.image,
  }));
  const deliveryFee = checkout.deliveryMethod === "express" ? 39 : 0;
  const totals = getTotals();
  let order = {
    orderNumber: `MR-${Date.now().toString(36).toUpperCase()}`,
    createdAt: new Date().toISOString(),
    items,
    checkout,
    subtotal: totals.subtotal,
    discount: totals.discount,
    shipping: totals.shipping + deliveryFee,
    total: totals.total + deliveryFee,
    paymentStatus: "演示支付已确认",
  };

  try {
    const response = await fetch("./api/orders", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        customer: {
          name: checkout.name,
          email: checkout.email,
          phone: checkout.phone,
        },
        delivery: {
          province: checkout.province,
          city: checkout.city,
          address: checkout.address,
          postalCode: checkout.postalCode,
        },
        items: cartItems.map((item) => ({
          productId: item.product.id,
          color: item.color,
          variant: item.variant,
          quantity: item.quantity,
        })),
        deliveryMethod: checkout.deliveryMethod,
        paymentMethod: checkout.paymentMethod,
        discountCode: state.discountApplied ? "MORROW10" : "",
        note: checkout.note || "",
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      const error = new Error(payload.error?.message || "订单创建失败");
      error.validation = true;
      throw error;
    }
    order = {
      ...payload.order,
      checkout,
    };
    state.catalogSource = "服务器库存接口";
  } catch (error) {
    if (error.validation) {
      state.paymentStage = "idle";
      renderCheckout();
      showToast("订单未提交", error.message, true);
      return;
    }
  }

  state.orders.unshift(order);
  state.lastOrder = order;
  state.cart = [];
  state.checkoutDraft = null;
  state.paymentStage = "idle";
  writeStorage(STORAGE_KEYS.orders, state.orders);
  persistCart();
  showToast("订单已创建", `订单号 ${order.orderNumber}`);
  navigate("confirmation");
  loadProductsFromApi(true);
}

function renderConfirmation() {
  const order = state.lastOrder || state.orders[0];
  if (!order) {
    navigate("store");
    return;
  }
  state.lastOrder = order;

  const deliveryStart = new Date(order.createdAt);
  const deliveryEnd = new Date(deliveryStart);
  deliveryEnd.setDate(deliveryEnd.getDate() + (order.checkout.deliveryMethod === "express" ? 2 : 5));
  const deliveryText = new Intl.DateTimeFormat("zh-CN", {
    month: "long",
    day: "numeric",
    weekday: "short",
  }).format(deliveryEnd);

  dom.confirmationView.innerHTML = `
    <div class="page-topline">
      <span class="back-button">
        <i data-lucide="circle-check" aria-hidden="true"></i>
        订单已创建
      </span>
      <span class="page-kicker">演示支付 / 无真实扣款</span>
    </div>

    <div class="confirmation-wrap">
      <div class="confirmation-hero">
        <span class="confirmation-icon">
          <i data-lucide="check" aria-hidden="true"></i>
        </span>
        <div>
          <p class="eyebrow">THANK YOU</p>
          <h1>订单已经确认。</h1>
          <p>
            这是模拟订单，支付状态仅用于展示流程。我们已将订单保存在当前浏览器中，
            不会产生真实扣款或配送。
          </p>
        </div>
      </div>

      <div class="confirmation-meta">
        <div>
          <span>订单编号</span>
          <strong data-confirmation-order-number>${escapeHtml(order.orderNumber)}</strong>
        </div>
        <div>
          <span>支付状态</span>
          <strong>${escapeHtml(order.paymentStatus)}</strong>
        </div>
        <div>
          <span>预计送达</span>
          <strong>${deliveryText}</strong>
        </div>
      </div>

      <section class="confirmation-order-panel" aria-label="订单号">
        <div>
          <p class="eyebrow">ORDER NUMBER</p>
          <h2>请保存这个订单号</h2>
          <p>之后可以直接在“我的”页面查看订单，也可以用订单号单独查询。</p>
        </div>
        <div class="confirmation-order-number">
          <span>订单号</span>
          <strong>${escapeHtml(order.orderNumber)}</strong>
          <button class="button button-secondary" type="button" data-action="copy-order" data-order-number="${escapeHtml(order.orderNumber)}">
            复制订单号
            <i data-lucide="copy" aria-hidden="true"></i>
          </button>
        </div>
      </section>

      <aside class="order-summary" style="margin-top: 34px; position: static; box-shadow: none;">
        <h2>订单内容</h2>
        <div class="summary-items">
          ${order.items
            .map(
              (item) => `
                <div class="summary-item">
                  <div class="summary-item-image">
                    <img src="${item.image}" alt="" width="1200" height="1500" />
                  </div>
                  <div>
                    <h3>${escapeHtml(item.name)}</h3>
                    <p>${escapeHtml(item.variantLabel || item.color)} / 数量 ${item.quantity}</p>
                  </div>
                  <strong>${formatCurrency(item.price * item.quantity)}</strong>
                </div>
              `,
            )
            .join("")}
        </div>
        <div class="summary-lines">
          <div class="summary-line">
            <span>商品小计</span>
            <span>${formatCurrency(order.subtotal)}</span>
          </div>
          ${
            order.discount > 0
              ? `
                <div class="summary-line">
                  <span>优惠</span>
                  <span>-${formatCurrency(order.discount)}</span>
                </div>
              `
              : ""
          }
          <div class="summary-line">
            <span>配送</span>
            <span>${order.shipping === 0 ? "免费" : formatCurrency(order.shipping)}</span>
          </div>
          <div class="summary-total">
            <span>合计</span>
            <strong>${formatCurrency(order.total)}</strong>
          </div>
        </div>
      </aside>

      <div class="confirmation-actions">
        <button class="button button-secondary" type="button" data-action="open-orders">
          进入我的订单
          <i data-lucide="receipt-text" aria-hidden="true"></i>
        </button>
        <button class="button button-primary" type="button" data-action="back-store">
          继续选购
          <i data-lucide="arrow-right" aria-hidden="true"></i>
        </button>
      </div>
    </div>
  `;
  refreshIcons();
}

function showOrders() {
  if (state.orders.length === 0) {
    showToast("暂无订单", "完成一次演示结账后，订单会显示在这里。", true);
    return;
  }
  const latest = state.orders[0];
  showToast(
    `最近订单 ${latest.orderNumber}`,
    `${latest.items.length} 种商品 / ${formatCurrency(latest.total)} / ${latest.paymentStatus}`,
  );
}

function resetCatalogFilters() {
  state.category = "all";
  state.sort = "featured";
  state.search = "";
  state.selectedBrand = "all";
  state.priceBand = "all";
  state.inStockOnly = false;
  state.visibleCount = 16;
  document.querySelectorAll("[data-category]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.category === "all");
  });
  const sort = document.querySelector("[data-sort]");
  if (sort) sort.value = "featured";
  if (dom.brandFilter) dom.brandFilter.value = "all";
  if (dom.priceFilter) dom.priceFilter.value = "all";
  if (dom.stockFilter) dom.stockFilter.checked = false;
  renderCatalog();
}

document.addEventListener("click", (event) => {
  const routeLink = event.target.closest("[data-route]");
  if (routeLink) {
    event.preventDefault();
    navigate(routeLink.dataset.route);
    return;
  }

  const scrollLink = event.target.closest("[data-scroll-target]");
  if (scrollLink) {
    event.preventDefault();
    scrollToSection(scrollLink.dataset.scrollTarget);
    closeMobileMenu(false);
    return;
  }

  const action = event.target.closest("[data-action]")?.dataset.action;
  if (action) {
    if (action === "open-cart") openCart();
    if (action === "close-cart") closeCart();
    if (action === "open-menu") openMobileMenu();
    if (action === "close-menu") closeMobileMenu();
    if (action === "open-search") openSearch();
    if (action === "close-search") closeSearch();
    if (action === "back-store") navigate("store");
    if (action === "show-featured") {
      state.category = "all";
      state.sort = "featured";
      state.visibleCount = 16;
      document.querySelectorAll("[data-category]").forEach((button) => {
        button.classList.toggle("is-active", button.dataset.category === "all");
      });
      const sort = document.querySelector("[data-sort]");
      if (sort) sort.value = "featured";
      renderCatalog();
      scrollToSection("catalog");
    }
    if (action === "load-more") {
      state.visibleCount += 16;
      renderCatalog();
      return;
    }
    if (action === "reset-search") resetCatalogFilters();
    if (action === "apply-discount") {
      const input = dom.cartFooter.querySelector("[data-discount-input]");
      const code = input?.value.trim().toUpperCase();
      if (code === "MORROW10") {
        state.discountApplied = true;
        writeStorage(STORAGE_KEYS.discount, true);
        renderCart();
        showToast("优惠已应用", "订单金额已减免 10%。");
      } else {
        showToast("优惠码无效", "请输入 MORROW10。", true);
      }
    }
    if (action === "checkout") {
      closeCart(false);
      if (getCartDetails().length === 0) {
        showToast("购物袋为空", "先选择商品，再进入结账。", true);
      } else {
        navigate("checkout");
      }
    }
    if (action === "add-product") {
      const product = productById(state.activeProductId);
      if (product) {
        addToCart(
          product.id,
          selectedColor(product),
          state.quantity,
          selectedVariants(product),
        );
      }
    }
    if (action === "open-orders") {
      window.location.href = "./orders.html";
    }
    if (action === "copy-order") {
      const orderNumber = event.target.closest("[data-order-number]")?.dataset.orderNumber;
      if (orderNumber && navigator.clipboard) {
        navigator.clipboard
          .writeText(orderNumber)
          .then(() => showToast("订单号已复制", orderNumber))
          .catch(() => showToast("复制失败", "请手动记录订单号。", true));
      }
    }
    return;
  }

  const categoryButton = event.target.closest("[data-category]");
  if (categoryButton) {
    state.category = categoryButton.dataset.category;
    state.visibleCount = 16;
    document.querySelectorAll("[data-category]").forEach((button) => {
      button.classList.toggle("is-active", button === categoryButton);
    });
    renderCatalog();
    return;
  }

  const quickAdd = event.target.closest("[data-add-quick]");
  if (quickAdd) {
    event.stopPropagation();
    const product = productById(quickAdd.dataset.addQuick);
    if (product) {
      addToCart(product.id, selectedColor(product), 1, selectedVariants(product));
    }
    return;
  }

  const productOpen = event.target.closest("[data-product-open]");
  if (productOpen) {
    navigate("product", productOpen.dataset.productOpen);
    return;
  }

  const galleryThumb = event.target.closest("[data-gallery-thumb]");
  if (galleryThumb && state.activeProductId) {
    state.galleryIndex = Number(galleryThumb.dataset.galleryThumb);
    renderProduct(state.activeProductId, true);
    return;
  }

  const colorOption = event.target.closest("[data-color-option]");
  if (colorOption && state.activeProductId) {
    state.selectedColors[state.activeProductId] = colorOption.dataset.colorOption;
    state.galleryIndex = 0;
    renderProduct(state.activeProductId, true);
    return;
  }

  const variantOptionButton = event.target.closest("[data-variant-option]");
  if (variantOptionButton && state.activeProductId) {
    const product = productById(state.activeProductId);
    const selections = selectedVariants(product);
    state.selectedVariants[state.activeProductId] = {
      ...selections,
      [variantOptionButton.dataset.variantGroup]:
        variantOptionButton.dataset.variantOption,
    };
    renderProduct(state.activeProductId, true);
    return;
  }

  const quantityButton = event.target.closest("[data-qty-change]");
  if (quantityButton && state.activeProductId) {
    const product = productById(state.activeProductId);
    const delta = Number(quantityButton.dataset.qtyChange);
    state.quantity = Math.max(1, Math.min(product.stock, state.quantity + delta));
    renderProduct(state.activeProductId, true);
    return;
  }

  const cartQuantityButton = event.target.closest("[data-cart-qty]");
  if (cartQuantityButton) {
    setCartQuantity(Number(cartQuantityButton.dataset.cartQty), Number(cartQuantityButton.dataset.qty));
    return;
  }

  const cartRemove = event.target.closest("[data-cart-remove]");
  if (cartRemove) {
    removeCartItem(Number(cartRemove.dataset.cartRemove));
    return;
  }

  const searchTerm = event.target.closest("[data-search-term]");
  if (searchTerm) {
    state.search = searchTerm.dataset.searchTerm;
    state.category = "all";
    state.visibleCount = 16;
    closeSearch();
    renderCatalog();
    scrollToSection("catalog");
    return;
  }

  if (event.target === dom.drawerScrim) {
    closeCart(false);
    closeMobileMenu(false);
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeCart();
    closeMobileMenu();
    closeSearch();
  }
});

document.addEventListener("change", (event) => {
  const target = event.target;
  if (target.matches("[data-sort]")) {
    state.sort = target.value;
    state.visibleCount = 16;
    renderCatalog();
  }

  if (target.matches("[data-brand-filter]")) {
    state.selectedBrand = target.value;
    state.visibleCount = 16;
    renderCatalog();
  }

  if (target.matches("[data-price-filter]")) {
    state.priceBand = target.value;
    state.visibleCount = 16;
    renderCatalog();
  }

  if (target.matches("[data-stock-filter]")) {
    state.inStockOnly = target.checked;
    state.visibleCount = 16;
    renderCatalog();
  }

  if (target.matches('input[name="deliveryMethod"], input[name="paymentMethod"]')) {
    const form = target.closest("[data-checkout-form]");
    const currentValues = form ? Object.fromEntries(new FormData(form).entries()) : {};
    state.checkoutDraft = {
      ...currentValues,
      [target.name]: target.value,
    };
    if (form) renderCheckout();
  }
});

document.addEventListener("submit", (event) => {
  if (!event.target.matches("[data-checkout-form]")) return;
  event.preventDefault();
  const checkout = validateCheckout(event.target);
  if (!checkout) {
    showToast("请检查表单", "部分配送信息尚未填写完整。", true);
    return;
  }
  state.checkoutDraft = checkout;
  state.paymentStage = "processing";
  renderCheckout();
  window.setTimeout(() => {
    if (state.paymentStage === "processing") completeOrder(checkout);
  }, 1100);
});

if (dom.searchInput) {
  dom.searchInput.addEventListener("keydown", (event) => {
    if (event.key !== "Enter") return;
    event.preventDefault();
    state.search = dom.searchInput.value.trim();
    state.category = "all";
    state.visibleCount = 16;
    closeSearch();
    renderCatalog();
    scrollToSection("catalog");
  });
}

window.addEventListener("hashchange", renderRoute);

populateBrandFilter();
renderCatalog();
renderCart();
parseRoute();
renderRoute();
refreshIcons();
loadProductsFromApi();
