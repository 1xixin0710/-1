from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright


BASE_URL = "http://127.0.0.1:4173"
SHOTS = Path(__file__).resolve().parents[1] / "work" / "system-screens"


def api(path: str, options: dict | None = None):
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        headers={"Content-Type": "application/json"},
        **(options or {}),
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def assert_site_chrome(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, locale="zh-CN")
    page = context.new_page()
    pages = [
        ("/index.html", "首页"),
        ("/admin/", "管理后台"),
        ("/orders/", None),
        ("/service/", None),
    ]
    expected_nav = ["首页", "实时好价", "全部商品", "管理后台", "AI 导购"]

    for path, active_label in pages:
        page.goto(f"{BASE_URL}{path}", wait_until="networkidle")
        page.wait_for_selector(".site-header")
        assert page.locator(".market-ribbon").count() == 1

        for width in (2334, 1440, 980, 390):
            page.set_viewport_size({"width": width, "height": 900})
            page.wait_for_timeout(40)
            metrics = page.evaluate(
                """
                () => {
                  const box = (selector) => {
                    const element = document.querySelector(selector);
                    if (!element || getComputedStyle(element).display === "none") return null;
                    const rect = element.getBoundingClientRect();
                    return {
                      y: rect.y,
                      height: rect.height,
                      center: rect.y + rect.height / 2,
                      display: getComputedStyle(element).display,
                    };
                  };
                  const header = box(".site-header");
                  return {
                    ribbon: box(".market-ribbon"),
                    header,
                    brand: box(".brand"),
                    nav: box(".desktop-nav"),
                    actions: box(".header-actions"),
                    menu: box(".mobile-menu-button"),
                    navItems: [...document.querySelectorAll(".desktop-nav > *")].map(
                      (element) => {
                        const rect = element.getBoundingClientRect();
                        return {
                          text: element.textContent.trim(),
                          center: rect.y + rect.height / 2,
                        };
                      },
                    ),
                    viewportWidth: window.innerWidth,
                    documentWidth: document.body.scrollWidth,
                  };
                }
                """
            )

            assert metrics["ribbon"]["height"] == 32
            assert metrics["header"]["height"] == 66
            assert metrics["documentWidth"] <= metrics["viewportWidth"] + 1
            assert [item["text"] for item in metrics["navItems"]] == expected_nav

            if width > 980:
                centers = [
                    metrics["header"]["center"],
                    metrics["brand"]["center"],
                    metrics["nav"]["center"],
                    metrics["actions"]["center"],
                ]
                assert max(centers) - min(centers) <= 1
                assert all(
                    abs(item["center"] - metrics["header"]["center"]) <= 1
                    for item in metrics["navItems"]
                )
            else:
                assert metrics["nav"] is None
                assert metrics["menu"]["display"] == "grid"

        if active_label:
            assert page.locator(".desktop-nav .is-active").text_content().strip() == active_label

        if path == "/admin/":
            page.set_viewport_size({"width": 1440, "height": 900})
            page.locator('.site-header [data-action="open-support"]').click()
            assert page.locator("[data-support-panel]").is_visible()
            page.locator("[data-service-trigger]").click()
            assert page.locator("[data-service-panel]").is_visible()
            assert not page.locator("[data-support-panel]").is_visible()

    context.close()


def run_desktop(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 1000}, locale="zh-CN")
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on(
        "console",
        lambda message: errors.append(message.text) if message.type == "error" else None,
    )

    page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
    page.wait_for_selector(".product-card")
    assert page.locator(".product-card").count() == 16
    assert "83" in page.locator("[data-catalog-meta]").inner_text()
    assert page.locator("[data-product-count]").inner_text().strip() == "83"
    assert page.locator("[data-brand-count]").inner_text().strip() == "31"
    assert "外设好物" in page.locator(".market-hotwords").inner_text()
    assert "桌面好物" not in page.locator(".market-hotwords").inner_text()
    page.locator('.filter-row [data-category="phone"]').click()
    page.wait_for_timeout(100)
    assert "25" in page.locator("[data-catalog-meta]").inner_text()
    page.locator('[data-action="load-more"]').click()
    page.wait_for_timeout(100)
    assert page.locator(".product-card").count() == 25

    page.locator('.site-header [data-action="open-search"]').click()
    page.locator("[data-search-input]").fill("相机")
    page.locator("[data-search-input]").press("Enter")
    page.wait_for_timeout(150)
    assert page.locator(".product-card").count() == 17
    assert "共 17 件商品" in page.locator("[data-catalog-meta]").inner_text()
    assert "当前显示 17 件" in page.locator("[data-catalog-meta]").inner_text()
    search_product_ids = page.locator(".product-card [data-product-open]").evaluate_all(
        "nodes => nodes.map(node => node.dataset.productOpen)"
    )
    assert search_product_ids
    assert all(product_id.startswith("camera-") for product_id in search_product_ids)

    page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
    page.locator('.site-header [data-action="open-search"]').click()
    page.locator("[data-search-input]").fill("GPW")
    page.locator("[data-search-input]").press("Enter")
    page.wait_for_timeout(150)
    gpw_cards = page.locator(".product-card")
    assert gpw_cards.count() == 2
    assert "GPW4（小狗" in gpw_cards.first.inner_text()
    assert "GPW5（Ultra" in gpw_cards.nth(1).inner_text()
    gpw_image_widths = page.locator(".product-card img").evaluate_all(
        "images => images.map(image => image.naturalWidth)"
    )
    assert gpw_image_widths and min(gpw_image_widths) >= 640

    page.locator('.site-header [data-action="open-search"]').click()
    page.locator("[data-search-input]").fill("GPW4 小狗")
    page.locator("[data-search-input]").press("Enter")
    page.wait_for_timeout(150)
    assert page.locator(".product-card").count() == 1
    assert "GPW4（小狗" in page.locator(".product-card").inner_text()

    page.locator('.site-header [data-action="open-search"]').click()
    page.locator("[data-search-input]").fill("GPW4小狗")
    page.locator("[data-search-input]").press("Enter")
    page.wait_for_timeout(150)
    assert page.locator(".product-card").count() == 1

    page.locator('.site-header [data-action="open-search"]').click()
    page.locator("[data-search-input]").fill("狗屁王")
    page.locator("[data-search-input]").press("Enter")
    page.wait_for_timeout(150)
    assert page.locator(".product-card").count() == 1

    page.locator('.site-header [data-action="open-search"]').click()
    page.locator("[data-search-input]").fill("EV63")
    page.locator("[data-search-input]").press("Enter")
    page.wait_for_timeout(150)
    assert page.locator(".product-card").count() == 1
    page.locator('.product-card [data-product-open="desk-iqunix-ev63"]').click()
    page.wait_for_selector('[data-action="add-product"]')
    assert "IQUNIX EV63 磁轴键盘" in page.locator(".product-info h1").inner_text()
    assert "机械键盘" not in page.locator(".product-info h1").inner_text()
    assert page.locator('[data-variant-group="switch"]').count() == 3
    assert page.locator("[data-color-option]").count() == 3
    page.locator('[data-variant-option="switch-magnetic-pro"]').click()
    assert "磁玉轴 Pro" in page.locator(".selected-variant-summary").inner_text()
    magnetic_price = int(
        re.sub(r"[^\d]", "", page.locator("[data-product-live-price]").inner_text())
    )
    assert 1300 <= magnetic_price <= 1400

    page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
    page.locator('.site-header [data-action="open-search"]').click()
    page.locator("[data-search-input]").fill("夜魔 Extreme")
    page.locator("[data-search-input]").press("Enter")
    page.wait_for_timeout(150)
    assert page.locator(".product-card").count() == 1
    page.locator('.product-card [data-product-open="desk-rog-azoth-extreme"]').click()
    page.wait_for_selector('[data-action="add-product"]')
    assert "ROG 夜魔 Extreme" in page.locator(".product-info h1").inner_text()
    assert page.locator('[data-variant-group="switch"]').count() == 2
    page.locator('[data-variant-option="switch-nx-storm"]').click()
    assert "NX 暴风蓝轴" in page.locator(".selected-variant-summary").inner_text()
    rog_price = int(
        re.sub(r"[^\d]", "", page.locator("[data-product-live-price]").inner_text())
    )
    assert 3500 <= rog_price <= 3700

    page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
    page.locator('.site-header [data-action="open-search"]').click()
    page.locator("[data-search-input]").fill("F87Pro")
    page.locator("[data-search-input]").press("Enter")
    page.wait_for_timeout(150)
    assert page.locator(".product-card").count() == 1
    page.locator('.product-card [data-product-open="desk-market-2181205"]').click()
    page.wait_for_selector('[data-action="add-product"]')
    assert page.locator('[data-variant-group="switch"]').count() == 2
    page.locator('[data-variant-option="switch-caramel-latte"]').click()
    assert "焦糖拿铁轴" in page.locator(".selected-variant-summary").inner_text()
    page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")

    page.locator(".category-dock [data-category=\"appliance\"]").click()
    page.wait_for_timeout(100)
    assert "5" in page.locator("[data-catalog-meta]").inner_text()
    assert page.locator(".product-card").count() == 5

    page.locator('.site-header [data-action="open-search"]').click()
    page.locator("[data-search-input]").fill("")
    page.locator("[data-search-input]").press("Enter")
    page.wait_for_timeout(100)

    page.locator('.category-dock [data-category="desk"]').click()
    page.wait_for_timeout(100)
    assert page.locator(".product-card").count() == 16
    assert "18" in page.locator("[data-catalog-meta]").inner_text()
    page.locator('[data-action="load-more"]').click()
    page.wait_for_timeout(100)
    assert page.locator(".product-card").count() == 18
    assert "桌面办公" not in page.locator("#catalog").inner_text()

    page.locator('.category-dock [data-category="audio"]').click()
    page.wait_for_timeout(100)
    assert page.locator(".product-card").count() == 6

    page.locator('.filter-row [data-category="all"]').click()
    page.locator('.filter-row [data-category="phone"]').click()
    page.locator("[data-brand-filter]").select_option(label="苹果")
    page.wait_for_timeout(100)
    assert page.locator(".product-card").count() == 3

    page.locator('.filter-row [data-category="all"]').click()
    page.locator("[data-brand-filter]").select_option("all")
    page.wait_for_timeout(100)
    page.locator('.site-header [data-action="open-search"]').click()
    page.locator("[data-search-input]").fill("iPhone 18 Pro")
    page.locator("[data-search-input]").press("Enter")
    page.wait_for_timeout(150)
    page.locator('.product-card [data-product-open="phone-anchor-2177308"]').click()
    page.wait_for_selector('[data-action="add-product"]')
    assert "iPhone 18 Pro" in page.locator(".product-info h1").inner_text()
    assert "参考价" in page.locator(".price-basis").inner_text()
    assert page.locator("[data-color-option]").count() == 4
    assert page.locator("[data-gallery-thumb]").count() == 3
    initial_gallery_image = page.locator(".gallery-main img").get_attribute("src")
    page.locator('[data-color-option="冰川蓝"]').click()
    assert "冰川蓝" in page.locator("[data-selected-color-label]").inner_text()
    glacier_gallery_image = page.locator(".gallery-main img").get_attribute("src")
    assert glacier_gallery_image != initial_gallery_image
    assert "iphone-18-pro-hero-glacier" in glacier_gallery_image
    page.locator('[data-gallery-thumb="1"]').click()
    assert page.locator(".gallery-counter").inner_text().strip() == "2 / 3"
    assert page.locator(".gallery-main img").get_attribute("src") != glacier_gallery_image
    page.locator('[data-variant-option="memory-16gb"]').click()
    page.locator('[data-variant-option="storage-512gb"]').click()
    assert "16GB / 512GB" in page.locator(".selected-variant-summary").inner_text()
    assert re.search(r"¥[\d,]+", page.locator("[data-product-live-price]").inner_text())

    product = api("/api/products/phone-anchor-2177308")["product"]
    previous_stock = product["stock"]
    page.locator('[data-action="add-product"]').click()
    page.wait_for_selector(".cart-drawer.is-open")
    assert page.locator(".cart-quantity output").inner_text().strip() == "1"
    page.locator('[data-action="checkout"]').click()
    page.wait_for_selector("[data-checkout-form]")

    page.locator("#checkout-name").fill("林墨")
    page.locator("#checkout-email").fill("linmo@example.com")
    page.locator("#checkout-phone").fill("13800138000")
    page.locator("#checkout-province").fill("浙江省")
    page.locator("#checkout-city").fill("杭州市")
    page.locator("#checkout-address").fill("西湖区文三路 88 号 6 楼")
    page.locator("#checkout-postal").fill("310000")
    page.locator('input[name="deliveryMethod"][value="express"]').check()
    page.wait_for_timeout(80)
    page.locator('input[name="paymentMethod"][value="alipay"]').check()
    page.wait_for_timeout(80)
    page.locator("[data-checkout-form] button[type='submit']").click()
    page.wait_for_selector(".confirmation-icon", timeout=7000)
    assert page.locator("[data-confirmation-order-number]").count() == 1
    assert page.locator(".confirmation-order-number").inner_text().strip()

    order_number = page.locator(".confirmation-meta strong").first.inner_text().strip()
    assert order_number.startswith("MR")
    order_payload = api(f"/api/orders?orderNumber={order_number}")["orders"][0]
    assert order_payload["items"][0]["variantLabel"] == "16GB / 512GB"
    assert abs(order_payload["items"][0]["price"] - 11899) <= 150
    assert order_payload["quoteAt"]
    after_order = api("/api/products/phone-anchor-2177308")["product"]
    assert after_order["stock"] == previous_stock - 1

    page.goto(f"{BASE_URL}/orders/", wait_until="networkidle")
    page.wait_for_selector(".order-result-card")
    assert page.locator(".order-result-card").count() >= 1
    page.locator('input[name="orderNumber"]').fill(order_number)
    page.locator("[data-order-lookup] button[type='submit']").click()
    page.wait_for_selector(".order-result-card")
    assert order_number in page.locator(".order-result-card").inner_text()
    assert "支付宝" in page.locator(".order-result-card").inner_text()

    page.goto(f"{BASE_URL}/admin/", wait_until="networkidle")
    page.locator('input[name="code"]').fill("2026")
    page.locator("[data-admin-login] button[type='submit']").click()
    page.wait_for_selector("#admin-console:not([hidden])")
    assert "83" in page.locator("#admin-kpis").inner_text()
    assert page.locator("#admin-order-rows tr").count() == 1

    page.locator("[data-admin-tab='orders']").click()
    page.locator("[data-order-status]").select_option("shipped")
    page.locator("[data-save-order]").click()
    page.wait_for_timeout(250)
    assert api(f"/api/orders?orderNumber={order_number}")["orders"][0]["status"] == "shipped"

    page.locator("[data-admin-tab='products']").click()
    first_stock = page.locator("[data-product-stock]").first
    old_value = int(first_stock.input_value())
    first_stock.fill(str(old_value + 2))
    page.locator("[data-save-product]").first.click()
    page.wait_for_timeout(250)
    assert "已" in page.locator("#admin-toast").inner_text()

    page.locator("[data-admin-tab='orders']").click()
    page.on("dialog", lambda dialog: dialog.accept())
    page.locator("[data-admin-reset]").click()
    page.wait_for_timeout(250)
    assert api("/api/orders?email=linmo@example.com")["orders"] == []

    support_ai_requests = []
    page.on(
        "request",
        lambda request: (
            support_ai_requests.append(request.url)
            if "text.pollinations.ai" in request.url
            else None
        ),
    )
    page.goto(f"{BASE_URL}/service/", wait_until="networkidle")
    assert page.locator("[data-service-trigger]").is_visible()
    assert page.locator("[data-support-trigger]").is_visible()
    assert page.locator('[data-action="open-customer-service"]').count() == 1
    page.locator("[data-service-trigger]").click()
    assert page.locator("[data-service-panel]").is_visible()
    assert not page.locator("[data-support-panel]").is_visible()
    page.locator("[data-service-form] input[name='message']").fill("多久发货")
    page.locator("[data-service-form]").press("Enter")
    page.wait_for_function(
        """
        () =>
          document.querySelector("[data-service-messages]").innerText.includes(
            "48 小时"
          )
        """,
        timeout=1800,
    )
    assert "售后客服" in page.locator("[data-service-messages]").inner_text()

    page.locator("[data-support-trigger]").click()
    assert page.locator("[data-support-panel]").is_visible()
    assert not page.locator("[data-service-panel]").is_visible()
    page.locator("[data-support-form] input[name='message']").fill("多久发货")
    page.locator("[data-support-form]").press("Enter")
    page.wait_for_function(
        """
        () =>
          document.querySelector("[data-support-messages]").innerText.includes(
            "售后客服"
          )
        """,
        timeout=1800,
    )
    assert "AI 导购只负责" in page.locator("[data-support-messages]").inner_text()

    bot_count = page.locator(
        "[data-support-messages] .support-message.is-bot:not(.support-typing)"
    ).count()
    page.locator("[data-support-form] input[name='message']").fill(
        "5000 元内拍照手机怎么选"
    )
    page.locator("[data-support-form]").press("Enter")
    page.wait_for_function(
        """
        (count) =>
          document.querySelectorAll(
            "[data-support-messages] .support-message.is-bot:not(.support-typing)"
          ).length > count
        """,
        arg=bot_count,
        timeout=1800,
    )
    assert "筛选" in page.locator("[data-support-messages]").inner_text()
    assert support_ai_requests == []

    for query, expected, forbidden in (
        ("1000键盘", "键盘", "鼠标"),
        ("1000鼠标", "鼠标", "键盘"),
        ("100键盘", "暂时没有", "¥"),
        ("G502", "G502 X PLUS", "键盘"),
    ):
        bot_count = page.locator(
            "[data-support-messages] .support-message.is-bot:not(.support-typing)"
        ).count()
        page.locator("[data-support-form] input[name='message']").fill(query)
        page.locator("[data-support-form]").press("Enter")
        page.wait_for_function(
            """
            (count) =>
              document.querySelectorAll(
                "[data-support-messages] .support-message.is-bot:not(.support-typing)"
              ).length > count
            """,
            arg=bot_count,
            timeout=1800,
        )
        reply = page.locator(
            "[data-support-messages] .support-message.is-bot:not(.support-typing)"
        ).last.inner_text()
        assert expected in reply
        assert forbidden not in reply
    assert support_ai_requests == []

    page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
    page.screenshot(path=str(SHOTS / "desktop-store.png"), full_page=True)
    assert errors == [], f"Browser errors: {errors}"
    context.close()


def run_mobile(browser):
    context = browser.new_context(
        viewport={"width": 390, "height": 844},
        device_scale_factor=1,
        is_mobile=True,
        has_touch=True,
        locale="zh-CN",
    )
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(f"{BASE_URL}/index.html", wait_until="networkidle")
    page.wait_for_selector(".product-card")

    assert page.locator("body").evaluate("el => el.scrollWidth <= window.innerWidth + 1")
    cards = page.locator(".product-card")
    for index in range(cards.count()):
        cards.nth(index).scroll_into_view_if_needed()
        page.wait_for_timeout(35)
    broken_images = page.locator("img").evaluate_all(
        """
        images => images
          .filter(image => !image.complete || image.naturalWidth === 0)
          .map(image => image.getAttribute("src"))
        """
    )
    assert broken_images == [], f"Broken images: {broken_images}"
    assert errors == [], f"Mobile errors: {errors}"

    page.goto(f"{BASE_URL}/orders/", wait_until="networkidle")
    assert page.locator("body").evaluate("el => el.scrollWidth <= window.innerWidth + 1")
    page.goto(f"{BASE_URL}/service/", wait_until="networkidle")
    assert page.locator("body").evaluate("el => el.scrollWidth <= window.innerWidth + 1")
    assert page.locator("[data-service-trigger] span").is_visible()
    assert page.locator("[data-support-trigger] span").is_visible()
    page.locator('[data-action="open-customer-service"]').click()
    assert page.locator("[data-service-panel]").is_visible()
    assert not page.locator("[data-support-panel]").is_visible()
    assert page.locator("body").evaluate("el => el.scrollWidth <= window.innerWidth + 1")
    page.locator("[data-support-trigger]").click()
    assert page.locator("[data-support-panel]").is_visible()
    assert not page.locator("[data-service-panel]").is_visible()
    assert page.locator("body").evaluate("el => el.scrollWidth <= window.innerWidth + 1")
    page.goto(f"{BASE_URL}/admin/", wait_until="networkidle")
    assert page.locator("body").evaluate("el => el.scrollWidth <= window.innerWidth + 1")

    page.screenshot(path=str(SHOTS / "mobile-admin.png"), full_page=False)
    context.close()


if __name__ == "__main__":
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch()
        assert_site_chrome(chromium)
        run_desktop(chromium)
        run_mobile(chromium)
        chromium.close()
    print("MORROW system smoke tests passed")
