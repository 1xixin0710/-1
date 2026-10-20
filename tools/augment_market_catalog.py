from __future__ import annotations

import io
import json
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from build_live_catalog import extract_brand, extract_listing_items, fetch_text
from catalog_variants import enrich_catalog


DATA_DIR = ROOT / "data"
IMAGE_DIR = ROOT / "assets" / "catalog"
MARKET_IMAGE_DIR = ROOT / "assets" / "market"
UPDATED_AT = "2026-10-19"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 Chrome/124 Safari/537.36"
)

CATEGORY_META = {
    "appliance": {
        "label": "家用电器",
        "series": "HOME",
        "colors": [
            {"name": "云白", "value": "#ecece7"},
            {"name": "钛灰", "value": "#737a7e"},
        ],
    },
    "audio": {
        "label": "耳机影音",
        "series": "AUDIO",
        "colors": [
            {"name": "曜石黑", "value": "#20242b"},
            {"name": "云母白", "value": "#e9e8e2"},
        ],
    },
    "tablet": {
        "label": "平板电脑",
        "series": "TABLET",
        "colors": [
            {"name": "深空灰", "value": "#4d5157"},
            {"name": "冰川银", "value": "#cfd3d7"},
        ],
    },
    "desk": {
        "label": "外设",
        "series": "DESK",
        "colors": [
            {"name": "石墨黑", "value": "#23262b"},
            {"name": "雾白", "value": "#e7e5df"},
        ],
    },
}


def fetch_html(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Referer": "https://www.zol.com.cn/",
            "Accept-Language": "zh-CN,zh;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=35) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def normalize_image_url(value: str) -> str:
    url = str(value or "").strip()
    if url.startswith("//"):
        return f"https:{url}"
    return url


def high_res_url(value: str) -> str:
    url = normalize_image_url(value)
    return re.sub(r"_\d+x\d+/", "_1000x750/", url)


def save_image(url: str, destination: Path) -> bool:
    if not url:
        return False
    request = urllib.request.Request(
        high_res_url(url),
        headers={"User-Agent": USER_AGENT, "Referer": "https://detail.zol.com.cn/"},
    )
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            body = response.read()
        image = Image.open(io.BytesIO(body)).convert("RGB")
    except Exception as error:
        print(f"  image failed: {high_res_url(url)} ({error})")
        return False
    if image.width < 640 or image.height < 480:
        print(f"  image too small: {image.size} {high_res_url(url)}")
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "JPEG", quality=91, optimize=True)
    return True


def parse_price(value: str) -> int | None:
    match = re.search(r"(\d+(?:\.\d+)?)", str(value or "").replace(",", ""))
    return round(float(match.group(1))) if match else None


def make_record(
    *,
    category: str,
    zol_id: str,
    title: str,
    price: int,
    image_url: str,
    product_url: str,
    list_url: str,
    rank: int,
) -> dict | None:
    meta = CATEGORY_META[category]
    destination = MARKET_IMAGE_DIR / f"{category}-{zol_id}.jpg"
    if not destination.exists() and not save_image(image_url, destination):
        return None

    compare_at = round(price * (1.10 + (rank % 4) * 0.02) / 10) * 10
    image_path = f"./{destination.relative_to(ROOT).as_posix()}"
    brand = extract_brand(title)
    return {
        "id": f"{category}-market-{zol_id}",
        "name": title,
        "series": f"{meta['label']} / {rank + 1:03d}",
        "category": category,
        "categoryLabel": meta["label"],
        "brand": brand,
        "price": price,
        "priceLabel": f"¥{price}",
        "compareAt": compare_at,
        "stock": 7 + ((rank * 13 + int(zol_id[-2:])) % 42),
        "sales": 4800 + rank * 1375,
        "rating": round(4.6 + (rank % 4) * 0.1, 1),
        "reviewCount": 520 + rank * 187,
        "featured": rank < 4,
        "description": (
            f"{meta['label']}热卖选品，公开报价与页面参数已核对。"
            "适合作为同价位商品的重点比较对象。"
        ),
        "materials": "官方标准配置，具体版本与参数以商品页和订单确认页为准。",
        "delivery": "现货商品预计 1 至 3 日送达，大件商品按地区预约配送。",
        "image": image_path,
        "colors": meta["colors"],
        "source": {
            "name": "ZOL 中关村在线",
            "url": product_url,
            "listUrl": list_url,
            "matchedTitle": title,
            "priceText": f"参考价 ¥{price}",
            "priceBasis": "ZOL 公开产品报价，实时价在此基础上作行情波动演示",
            "updatedAt": UPDATED_AT,
            "note": "价格会随地区、版本和促销活动变化，支付入口仅作演示。",
        },
    }


def parse_rank_page(url: str, category: str, limit: int) -> list[dict]:
    soup = BeautifulSoup(fetch_html(url), "html.parser")
    records = []
    seen = set()
    for item in soup.select("ul.rank-list li"):
        title_link = item.select_one(".title a[href*='detail.zol.com.cn']")
        price_node = item.select_one(".price")
        image = item.select_one("img")
        if not title_link or not price_node or not image:
            continue
        title = title_link.get("title") or title_link.get_text(" ", strip=True)
        price = parse_price(price_node.get_text(" ", strip=True))
        product_id_match = re.search(r"/index(\d+)\.shtml", title_link.get("href", ""))
        if not price or not product_id_match or product_id_match.group(1) in seen:
            continue
        seen.add(product_id_match.group(1))
        record = make_record(
            category=category,
            zol_id=product_id_match.group(1),
            title=title,
            price=price,
            image_url=image.get("src", ""),
            product_url=normalize_image_url(title_link.get("href", "")),
            list_url=url,
            rank=len(records),
        )
        if record:
            records.append(record)
        if len(records) >= limit:
            break
    return records


def parse_tablet_page(url: str, limit: int) -> list[dict]:
    soup = BeautifulSoup(fetch_html(url), "html.parser")
    records = []
    seen = set()
    for item in soup.select(".editors-recommend .slide-item"):
        link = item.select_one("a[href*='detail.zol.com.cn']")
        image = item.select_one("img")
        title_node = item.select_one(".r-slide-txt")
        price_node = item.select_one(".bottom-info font")
        if not link or not image or not title_node or not price_node:
            continue
        title = title_node.get_text(" ", strip=True)
        price = parse_price(price_node.get_text(" ", strip=True))
        product_id_match = re.search(r"/index(\d+)\.shtml", link.get("href", ""))
        if not price or not product_id_match or product_id_match.group(1) in seen:
            continue
        seen.add(product_id_match.group(1))
        record = make_record(
            category="tablet",
            zol_id=product_id_match.group(1),
            title=title,
            price=price,
            image_url=image.get("src", ""),
            product_url=normalize_image_url(link.get("href", "")),
            list_url=url,
            rank=len(records),
        )
        if record:
            records.append(record)
        if len(records) >= limit:
            break
    return records


def parse_listing_page(
    url: str,
    category: str,
    limit: int,
    offset: int = 0,
) -> list[dict]:
    items = extract_listing_items(fetch_text(url), url)
    records = []
    for item in items[offset : offset + limit]:
        record = make_record(
            category=category,
            zol_id=item["zol_id"],
            title=item["title"],
            price=item["price"],
            image_url=item["image_url"],
            product_url=item["product_url"],
            list_url=url,
            rank=len(records),
        )
        if record:
            records.append(record)
    return records


def add_market_products(catalog: list[dict]) -> list[dict]:
    existing_ids = {str(item.get("id")) for item in catalog}
    sources = [
        ("https://headphone.zol.com.cn/", "audio", 12),
        ("https://air.zol.com.cn/", "appliance", 8),
        ("https://detail.zol.com.cn/speaker/", "audio", 8),
        ("https://detail.zol.com.cn/keyboard/", "desk", 8),
        ("https://detail.zol.com.cn/mice/", "desk", 8),
    ]
    additions = []
    for url, category, limit in sources:
        print(f"Reading {category}: {url}")
        try:
            additions.extend(parse_rank_page(url, category, limit))
        except Exception as error:
            print(f"  rank parse failed: {error}")
        if url != "https://headphone.zol.com.cn/":
            try:
                additions.extend(parse_listing_page(url, category, limit))
            except Exception as error:
                print(f"  listing parse failed: {error}")
        time.sleep(0.35)

    print("Reading tablet: https://pad.zol.com.cn/")
    additions.extend(parse_tablet_page("https://pad.zol.com.cn/", 10))

    # The rank/list variants occasionally produce duplicate product ids.
    unique = []
    for product in additions:
        if product["id"] in existing_ids:
            continue
        existing_ids.add(product["id"])
        unique.append(product)
    return catalog + unique


def find_high_res_image(html: str) -> str | None:
    matches = re.findall(
        r"(?:https?:)?//[^\"'\s]+zol-img\.com\.cn/product/\d+_\d+x\d+/\d+/[\w-]+\.(?:jpg|jpeg|png|webp)",
        html,
        flags=re.IGNORECASE,
    )
    if not matches:
        return None
    return high_res_url(matches[0])


def upgrade_existing_image(product: dict) -> tuple[str, bool]:
    image_path = ROOT / str(product.get("image", "")).removeprefix("./")
    if not image_path.exists():
        return str(product.get("id")), False
    try:
        with Image.open(image_path) as image:
            if image.width >= 800:
                return str(product.get("id")), False
    except Exception:
        return str(product.get("id")), False
    product_url = str(product.get("source", {}).get("url") or "")
    if "detail.zol.com.cn" not in product_url:
        return str(product.get("id")), False
    try:
        url = find_high_res_image(fetch_html(product_url))
        if not url:
            return str(product.get("id")), False
        request = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT, "Referer": product_url},
        )
        with urllib.request.urlopen(request, timeout=35) as response:
            body = response.read()
        image = Image.open(io.BytesIO(body)).convert("RGB")
        if image.width < 640 or image.height < 480:
            return str(product.get("id")), False
        image.save(image_path, "JPEG", quality=91, optimize=True)
        return str(product.get("id")), True
    except Exception as error:
        print(f"  upgrade failed {product.get('id')}: {error}")
        return str(product.get("id")), False


def upgrade_catalog_images(catalog: list[dict]) -> None:
    targets = [
        product
        for product in catalog
        if "detail.zol.com.cn" in str(product.get("source", {}).get("url") or "")
    ]
    print(f"Upgrading {len(targets)} public product images")
    upgraded = 0
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(upgrade_existing_image, product) for product in targets]
        for future in as_completed(futures):
            product_id, changed = future.result()
            if changed:
                upgraded += 1
                print(f"  high-res: {product_id}")
    print(f"Upgraded {upgraded} images")


def main() -> None:
    catalog_path = DATA_DIR / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog = add_market_products(catalog)
    upgrade_catalog_images(catalog)
    catalog = enrich_catalog(catalog)

    catalog_path.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (DATA_DIR / "catalog.js").write_text(
        "window.MORROW_PRODUCTS = "
        + json.dumps(catalog, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(catalog)} products")


if __name__ == "__main__":
    main()
