from __future__ import annotations

import json
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
    assert "54" in page.locator("[data-catalog-meta]").inner_text()
    assert page.locator('[data-product-open="phone-anchor-2177308"]').count() == 1

    page.locator('[data-category="phone"]').click()
    page.wait_for_timeout(100)
    assert "25" in page.locator("[data-catalog-meta]").inner_text()
    page.locator('[data-action="load-more"]').click()
    page.wait_for_timeout(100)
    assert page.locator(".product-card").count() == 25

    page.locator("[data-brand-filter]").select_option(label="苹果")
    page.wait_for_timeout(100)
    assert page.locator(".product-card").count() == 3

    page.locator('[data-category="all"]').click()
    page.locator("[data-brand-filter]").select_option("all")
    page.wait_for_timeout(100)
    page.locator('[data-product-open="phone-anchor-2177308"]').click()
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
    assert "¥11,899" in page.locator(".product-price-line").inner_text()

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
    assert order_payload["items"][0]["price"] == 11899
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
    assert "54" in page.locator("#admin-kpis").inner_text()
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

    page.goto(f"{BASE_URL}/service/", wait_until="networkidle")
    page.locator("[data-support-trigger]").click()
    page.locator("[data-support-form] input[name='message']").fill("多久发货")
    page.locator("[data-support-form]").press("Enter")
    assert "48 小时" in page.locator("[data-support-messages]").inner_text()

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
    page.locator("[data-support-trigger]").click()
    assert page.locator("[data-support-panel]").is_visible()
    assert page.locator("body").evaluate("el => el.scrollWidth <= window.innerWidth + 1")
    page.goto(f"{BASE_URL}/admin/", wait_until="networkidle")
    assert page.locator("body").evaluate("el => el.scrollWidth <= window.innerWidth + 1")

    page.screenshot(path=str(SHOTS / "mobile-admin.png"), full_page=False)
    context.close()


if __name__ == "__main__":
    SHOTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch()
        run_desktop(chromium)
        run_mobile(chromium)
        chromium.close()
    print("MORROW system smoke tests passed")
