from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
IMAGE_DIR = ROOT / "assets" / "catalog"

SOURCES = [
    {
        "key": "phone",
        "label": "手机",
        "urls": [
            "https://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html",
            "https://detail.zol.com.cn/cell_phone_index/subcate57_list_2.html",
        ],
        "limit": 16,
    },
    {
        "key": "laptop",
        "label": "电脑办公",
        "urls": [
            "https://detail.zol.com.cn/notebook_index/subcate16_list_1.html",
            "https://detail.zol.com.cn/notebook_index/subcate16_list_2.html",
        ],
        "limit": 14,
    },
    {
        "key": "camera",
        "label": "摄影器材",
        "urls": [
            "https://detail.zol.com.cn/digital_camera_index/subcate15_list_1.html",
        ],
        "limit": 10,
    },
    {
        "key": "appliance",
        "label": "家用电器",
        "urls": [
            "https://detail.zol.com.cn/washer/",
            "https://detail.zol.com.cn/air_conditioner/",
        ],
        "limit": 10,
    },
]

BRANDS = [
    "苹果",
    "Apple",
    "华为",
    "HUAWEI",
    "小米",
    "Redmi",
    "荣耀",
    "vivo",
    "OPPO",
    "一加",
    "真我",
    "三星",
    "联想",
    "惠普",
    "华硕",
    "戴尔",
    "ThinkPad",
    "机械革命",
    "佳能",
    "索尼",
    "尼康",
    "富士",
    "松下",
    "海尔",
    "小天鹅",
    "美的",
    "西门子",
    "格力",
    "TCL",
    "卡萨帝",
]

COLOR_SETS = {
    "phone": [
        {"name": "基础色", "value": "#252a32"},
        {"name": "浅色", "value": "#d7d9dc"},
    ],
    "laptop": [
        {"name": "深空灰", "value": "#4d5157"},
        {"name": "银灰", "value": "#c6c8cb"},
    ],
    "camera": [
        {"name": "经典黑", "value": "#17191d"},
        {"name": "银黑", "value": "#a8aaae"},
    ],
    "appliance": [
        {"name": "雪白", "value": "#ecece7"},
        {"name": "钛灰", "value": "#737a7e"},
    ],
}


def parse_price(value: str) -> int | None:
    clean = value.replace(",", "").replace("￥", "").replace("¥", "").strip()
    if not clean or "概念" in clean:
        return None
    range_parts = re.split(r"[-至]", clean)
    first = range_parts[0]
    match = re.search(r"(\d+(?:\.\d+)?)", first)
    if not match:
        return None
    number = float(match.group(1))
    if "万" in first:
        number *= 10000
    return int(number)


def extract_brand(title: str) -> str:
    lowered = title.lower()
    for brand in BRANDS:
        if brand.lower() in lowered:
            aliases = {
                "Apple": "苹果",
                "HUAWEI": "华为",
                "Redmi": "小米",
                "真我": "realme",
            }
            return aliases.get(brand, brand)
    return "其他品牌"


def download_image(url: str, destination_stem: Path) -> str | None:
    if not url:
        return None
    if url.startswith("//"):
        url = f"https:{url}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")
            body = response.read()
    except Exception as error:
        print(f"Image failed: {url} ({error})")
        return None

    extension = ".jpg"
    if "png" in content_type:
        extension = ".png"
    elif "webp" in content_type:
        extension = ".webp"

    destination = destination_stem.with_suffix(extension)
    destination.write_bytes(body)
    return str(destination.relative_to(ROOT)).replace("\\", "/")


def extract_page(page, source, start_index: int, limit: int):
    items = page.locator("#J_PicMode > li")
    if items.count() == 0:
        items = page.locator("li").filter(has=page.locator(".price-row"))

    records = []
    for index in range(items.count()):
        if len(records) >= limit:
            break

        item = items.nth(index)
        title_link = item.locator("h3 a").first
        if title_link.count() == 0:
            continue

        title = (title_link.get_attribute("title") or title_link.inner_text()).strip()
        title = re.sub(r"\s+", " ", title)
        price_text = (
            item.locator(".price-type").first.inner_text().strip()
            if item.locator(".price-type").count()
            else ""
        )
        price = parse_price(price_text)
        if not title or price is None:
            continue

        product_link = urljoin(page.url, title_link.get_attribute("href") or "")
        image = item.locator("img").first
        image_url = ""
        if image.count():
            image_url = image.evaluate(
                "element => element.currentSrc || element.src || element.dataset.src || ''"
            )
        if not image_url or "b2c-icon" in image_url:
            continue

        child_text = title_link.evaluate(
            """
            element => Array.from(element.childNodes)
              .map(node => node.textContent || "")
              .join(" ")
              .replace(/\\s+/g, " ")
              .trim()
            """
        )
        tagline = child_text.replace(title, "", 1).strip()
        if not tagline:
            tagline = f"{source['label']}热门型号，平台参考价随地区与活动变动。"

        specs = []
        spec_labels = item.locator(".core-param-label span")
        for spec_index in range(spec_labels.count()):
            spec = spec_labels.nth(spec_index).inner_text().replace("\n", " ").strip()
            if spec:
                specs.append(spec)

        sequence = start_index + len(records) + 1
        filename = f"zol-{source['key']}-{sequence:03d}"
        image_path = download_image(image_url, IMAGE_DIR / filename)
        if not image_path:
            continue

        brand = extract_brand(title)
        material_text = "、".join(specs) if specs else "官方标准配置"
        record = {
            "id": f"{source['key']}-{sequence:03d}",
            "name": title,
            "series": f"{source['label']} / {sequence:03d}",
            "category": source["key"],
            "categoryLabel": source["label"],
            "brand": brand,
            "price": price,
            "priceLabel": price_text,
            "compareAt": int(round(price * 1.08 / 10) * 10),
            "stock": 8 + ((sequence * 7) % 34),
            "sales": 3800 - sequence * 67,
            "rating": round(4.6 + ((sequence % 4) * 0.1), 1),
            "reviewCount": 120 + sequence * 37,
            "featured": sequence <= 4,
            "description": tagline,
            "materials": material_text,
            "delivery": (
                "现货商品由平台仓或品牌仓发出，预计 1 至 3 日送达。"
                "偏远地区时效可能增加 1 至 2 日。"
            ),
            "image": f"./{image_path}",
            "colors": COLOR_SETS[source["key"]],
            "source": {
                "name": "ZOL 中关村在线",
                "url": product_link,
                "priceText": price_text,
                "updatedAt": "2026-09-28",
            },
        }
        records.append(record)

    return records


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    catalog = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            locale="zh-CN",
            viewport={"width": 1365, "height": 900},
        )

        for source in SOURCES:
            source_records = []
            for url in source["urls"]:
                if len(source_records) >= source["limit"]:
                    break
                print(f"Importing {source['label']}: {url}")
                page.goto(url, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(1200)
                source_records.extend(
                    extract_page(
                        page,
                        source,
                        start_index=len(source_records),
                        limit=source["limit"] - len(source_records),
                    )
                )
                time.sleep(2)
            catalog.extend(source_records)
            print(f"Imported {len(source_records)} {source['label']} products")

        browser.close()

    catalog_path = DATA_DIR / "catalog.json"
    catalog_path.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    catalog_js = DATA_DIR / "catalog.js"
    catalog_js.write_text(
        "window.MORROW_PRODUCTS = "
        + json.dumps(catalog, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(catalog)} products to {catalog_path}")


if __name__ == "__main__":
    main()
