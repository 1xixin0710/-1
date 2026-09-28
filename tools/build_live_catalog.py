from __future__ import annotations

import html
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from catalog_variants import enrich_catalog


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
IMAGE_DIR = ROOT / "assets" / "catalog"
UPDATED_AT = "2026-09-28"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CATEGORY_LABELS = {
    "phone": "手机数码",
    "computer": "电脑办公",
    "camera": "摄影器材",
    "appliance": "家用电器",
}

COLOR_SETS = {
    "phone": [
        {"name": "曜石黑", "value": "#20242b"},
        {"name": "云雾白", "value": "#e8e7e2"},
    ],
    "computer": [
        {"name": "深空灰", "value": "#4d5157"},
        {"name": "月光银", "value": "#c8cacc"},
    ],
    "camera": [
        {"name": "经典黑", "value": "#17191d"},
        {"name": "银黑", "value": "#a8aaae"},
    ],
    "appliance": [
        {"name": "云白", "value": "#ecece7"},
        {"name": "钛灰", "value": "#737a7e"},
    ],
}

SOURCES = [
    {
        "key": "phone",
        "label": "手机数码",
        "urls": [
            "https://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html",
            "https://detail.zol.com.cn/cell_phone_index/subcate57_list_2.html",
        ],
        "limit": 24,
    },
    {
        "key": "computer",
        "label": "电脑办公",
        "urls": [
            "https://detail.zol.com.cn/notebook_index/subcate16_list_1.html",
            "https://detail.zol.com.cn/notebook_index/subcate16_list_2.html",
        ],
        "limit": 18,
    },
    {
        "key": "camera",
        "label": "摄影器材",
        "urls": [
            "https://detail.zol.com.cn/digital_camera_index/subcate15_list_1.html",
            "https://detail.zol.com.cn/digital_camera_index/subcate15_list_2.html",
        ],
        "limit": 16,
    },
    {
        "key": "appliance",
        "label": "家用电器",
        "urls": [
            "https://detail.zol.com.cn/washer/",
            "https://detail.zol.com.cn/air-condition/",
            "https://detail.zol.com.cn/sweeping_robot/",
            "https://detail.zol.com.cn/digital_tv/",
        ],
        "limit_per_url": 5,
        "limit": 20,
    },
]

BRAND_ALIASES = [
    ("苹果", ("apple", "苹果", "iphone", "macbook")),
    ("华为", ("huawei", "华为", "matebook", "pura")),
    ("小米", ("小米", "xiaomi", "redmi", "米家")),
    ("三星", ("samsung", "三星")),
    ("荣耀", ("荣耀", "honor")),
    ("vivo", ("vivo", "iqoo")),
    ("OPPO", ("oppo", "一加", "oneplus", "realme", "真我")),
    ("联想", ("联想", "lenovo", "thinkpad", "拯救者")),
    ("惠普", ("惠普", "hp")),
    ("华硕", ("华硕", "asus", "rog")),
    ("戴尔", ("戴尔", "dell")),
    ("机械革命", ("机械革命",)),
    ("佳能", ("佳能", "canon")),
    ("索尼", ("索尼", "sony")),
    ("尼康", ("尼康", "nikon")),
    ("富士", ("富士", "fujifilm")),
    ("松下", ("松下", "panasonic")),
    ("海尔", ("海尔", "haier")),
    ("卡萨帝", ("卡萨帝", "casarte")),
    ("小天鹅", ("小天鹅", "littleswan")),
    ("美的", ("美的", "midea")),
    ("格力", ("格力", "gree")),
    ("TCL", ("tcl",)),
    ("海信", ("海信", "hisense")),
    ("石头", ("石头", "roborock")),
    ("科沃斯", ("科沃斯", "ecovacs")),
    ("追觅", ("追觅", "dreame")),
]


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/124 Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=35) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def parse_price(value: str) -> int | None:
    clean = value.replace(",", "").replace("￥", "").replace("¥", "").strip()
    if not clean or "暂无" in clean or "概念" in clean:
        return None
    match = re.search(r"(\d+(?:\.\d+)?)", clean)
    if not match:
        return None
    number = float(match.group(1))
    if "万" in clean:
        number *= 10000
    return int(number)


def extract_brand(title: str) -> str:
    lowered = title.lower()
    for brand, aliases in BRAND_ALIASES:
        if any(alias in lowered for alias in aliases):
            return brand
    return "精选品牌"


def download_image(url: str, destination_stem: Path) -> Path | None:
    if not url:
        return None
    for existing in IMAGE_DIR.glob(f"{destination_stem.name}.*"):
        if existing.is_file() and existing.stat().st_size >= 2500:
            return existing
    if url.startswith("//"):
        url = f"https:{url}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 Chrome/124 Safari/537.36"
            ),
            "Referer": "https://detail.zol.com.cn/",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=35) as response:
            content_type = response.headers.get("Content-Type", "")
            body = response.read()
    except Exception as error:
        print(f"Image failed: {url} ({error})")
        return None

    if len(body) < 2500:
        print(f"Image too small: {url} ({len(body)} bytes)")
        return None

    extension = ".jpg"
    if "png" in content_type:
        extension = ".png"
    elif "webp" in content_type:
        extension = ".webp"
    destination = destination_stem.with_suffix(extension)
    destination.write_bytes(body)
    return destination


def extract_listing_items(page: str, page_url: str) -> list[dict]:
    blocks = re.findall(
        r'<li\s+data-follow-id="([^"]+)"[^>]*>(.*?)</li>',
        page,
        flags=re.DOTALL,
    )
    items: list[dict] = []
    for follow_id, block in blocks:
        title_match = re.search(
            r'<h3>\s*<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>\s*</h3>',
            block,
            flags=re.DOTALL,
        )
        image_match = re.search(
            r'class="pic"[^>]*>.*?<img[^>]+(?:src|\.src)="([^"]+)"',
            block,
            flags=re.DOTALL,
        )
        price_match = re.search(
            r'<b class="price-type">([^<]+)</b>',
            block,
        )
        if not title_match or not image_match or not price_match:
            continue

        raw_title = title_match.group(2)
        tagline_match = re.search(r"<span>(.*?)</span>", raw_title, flags=re.DOTALL)
        title = clean_text(re.sub(r"<span>.*?</span>", "", raw_title, flags=re.DOTALL))
        tagline = clean_text(tagline_match.group(1)) if tagline_match else ""
        price = parse_price(clean_text(price_match.group(1)))
        if not title or price is None:
            continue

        score_match = re.search(r'<span class="score">([^<]+)</span>', block)
        review_match = re.search(r'<a class="comment-num"[^>]*>(\d+)人点评</a>', block)
        image_url = html.unescape(image_match.group(1))
        if image_url.startswith("//"):
            image_url = f"https:{image_url}"

        product_url = urllib.parse.urljoin(page_url, title_match.group(1))
        items.append(
            {
                "zol_id": follow_id.removeprefix("p"),
                "title": title,
                "tagline": tagline,
                "price": price,
                "score": float(score_match.group(1)) if score_match else 0,
                "review_count": int(review_match.group(1)) if review_match else 0,
                "image_url": image_url,
                "product_url": product_url,
            }
        )
    return items


def build_record(item: dict, source: dict, sequence: int, source_page: str) -> dict | None:
    destination_stem = IMAGE_DIR / f"{source['key']}-{sequence:03d}-{item['zol_id']}"
    image_path = download_image(item["image_url"], destination_stem)
    if not image_path:
        return None

    relative_image = str(image_path.relative_to(ROOT)).replace("\\", "/")
    description = item["tagline"] or (
        f"来自 2026 热门榜单的{source['label']}商品，适合日常高频使用和长期持有。"
    )
    if item["score"] and item["review_count"]:
        popularity = f"榜单评分 {item['score']:.1f}，{item['review_count']} 人点评。"
    elif item["score"]:
        popularity = f"榜单评分 {item['score']:.1f}。"
    else:
        popularity = "新品关注度较高。"

    return {
        "id": f"{source['key']}-{sequence:03d}-{item['zol_id']}",
        "name": item["title"],
        "series": f"{source['label']} / {sequence:03d}",
        "category": source["key"],
        "categoryLabel": source["label"],
        "brand": extract_brand(item["title"]),
        "price": item["price"],
        "priceLabel": f"¥{item['price']}",
        "compareAt": None,
        "stock": 8 + ((sequence * 11) % 39),
        "sales": max(860, 32000 - sequence * 317),
        "rating": item["score"] or round(4.6 + ((sequence % 4) * 0.1), 1),
        "reviewCount": item["review_count"] or 180 + sequence * 43,
        "featured": sequence <= 3,
        "description": f"{description} {popularity}",
        "materials": "官方标准配置，具体版本与参数以商品页和订单确认页为准。",
        "delivery": "现货商品预计 1 至 3 日送达，大件家电按地区预约安装。",
        "image": f"./{relative_image}",
        "colors": COLOR_SETS[source["key"]],
        "source": {
            "name": "ZOL 中关村在线",
            "url": item["product_url"],
            "listUrl": source_page,
            "matchedTitle": item["title"],
            "priceText": f"参考价 ¥{item['price']}",
            "priceBasis": "ZOL 中关村在线公开产品报价，价格随地区与促销变化",
            "updatedAt": UPDATED_AT,
            "note": "本页价格为公开参考价，不是实时成交价；支付入口仅作演示。",
        },
    }


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    catalog: list[dict] = []
    sequence = 0
    used_products: set[str] = set()
    catalog_path = DATA_DIR / "catalog.json"
    previous_catalog = []
    if catalog_path.exists():
        try:
            previous_catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous_catalog = []

    for source in SOURCES:
        source_count = 0
        for source_page in source["urls"]:
            if source_count >= source["limit"]:
                break
            print(f"Reading {source['label']}: {source_page}")
            page = fetch_text(source_page)
            items = extract_listing_items(page, source_page)
            page_limit = source.get("limit_per_url", source["limit"])
            page_count = 0
            for item in items:
                if page_count >= page_limit or source_count >= source["limit"]:
                    break
                if item["zol_id"] in used_products:
                    continue
                sequence += 1
                record = build_record(item, source, sequence, source_page)
                if not record:
                    sequence -= 1
                    continue
                used_products.add(item["zol_id"])
                catalog.append(record)
                source_count += 1
                page_count += 1
                print(
                    f"  {record['name']} / ¥{record['price']} / {record['brand']}"
                )
                time.sleep(0.12)
            time.sleep(0.5)

    anchors = [
        {
            "zol_id": "2177308",
            "title": "苹果iPhone 18 Pro（256GB）",
            "tagline": "iPhone 实力巅峰，性能与摄像头表现满级，电池续航大进化",
            "price": 9999,
            "score": 0,
            "review_count": 0,
            "image_url": (
                "https://2b.zol-img.com.cn/product/276_500x375/919/cewnUwqgMGCa.jpg"
            ),
            "product_url": "https://detail.zol.com.cn/cell_phone/index2177308.shtml",
        }
    ]
    anchor_source = {
        "key": "phone",
        "label": "手机数码",
    }
    for anchor in anchors:
        sequence += 1
        destination_stem = IMAGE_DIR / f"phone-anchor-{anchor['zol_id']}"
        image_path = download_image(anchor["image_url"], destination_stem)
        if not image_path:
            sequence -= 1
            continue
        record = build_record(anchor, anchor_source, sequence, anchor["product_url"])
        if record:
            record["id"] = f"phone-anchor-{anchor['zol_id']}"
            record["featured"] = True
            catalog.insert(0, record)

    legacy_overrides = {
        "computer-apple-macbook-air-m4": {
            "name": "Apple MacBook Air 13 英寸 M4 16GB+256GB",
            "price": 7999,
            "sourceTitle": "MacBook Air M4 13英寸",
        },
        "computer-apple-macbook-pro-14-m4-pro": {
            "name": "Apple MacBook Neo 13 英寸 A18 Pro 8GB+256GB",
            "price": 4599,
            "sourceTitle": "Apple MacBook Neo 13英寸 A18 Pro 8GB 256GB",
        },
        "computer-honor-magicbook-x16-pro": {
            "name": "荣耀 MagicBook X16 Pro 2025",
            "price": 3999,
            "sourceTitle": "荣耀 MagicBook X16 Pro",
        },
        "computer-rog-zephyrus-g14": {
            "name": "ROG 幻 14 Air 2026 酷睿 Ultra 9 RTX 5070",
            "price": 14999,
            "sourceTitle": "ROG幻14 Air 2026 酷睿U9 14英寸游戏本",
        },
        "computer-asus-tianxuan-6": {
            "name": "华硕天选 7 Pro 酷睿版 RTX 5060",
            "price": 8900,
            "sourceTitle": "华硕天选7 Pro 酷睿版 16英寸游戏本 RTX5060",
        },
        "computer-hp-omen-10": {
            "name": "惠普暗影精灵 10 游戏本",
            "price": 7999,
            "sourceTitle": "惠普 暗影精灵10",
        },
        "computer-lenovo-xiaoxin-pro-14": {
            "name": "联想小新 Pro 14c 锐龙 7 H255 24GB+1TB",
            "price": 5299,
            "sourceTitle": "联想小新Pro14c 14英寸轻薄笔记本电脑",
        },
        "computer-thinkpad-x1-carbon-13": {
            "name": "联想 ThinkPad E14 2.8K AI 商务本",
            "price": 7999,
            "sourceTitle": "联想ThinkPad E14 BHCD 14英寸2.8K AI商务办公轻薄本",
        },
    }
    existing_ids = {item["id"] for item in catalog}
    previous_by_id = {item.get("id"): item for item in previous_catalog}
    for legacy_id, override in legacy_overrides.items():
        legacy = previous_by_id.get(legacy_id)
        if not legacy or legacy_id in existing_ids:
            continue
        record = dict(legacy)
        record.update(
            {
                "id": legacy_id,
                "name": override["name"],
                "price": override["price"],
                "priceLabel": f"¥{override['price']}",
                "featured": False,
                "category": "computer",
                "categoryLabel": "电脑办公",
                "series": f"电脑办公 / {len([item for item in catalog if item['category'] == 'computer']) + 1:03d}",
            }
        )
        record["source"] = {
            **record.get("source", {}),
            "name": "ZOL / 苏宁公开页面核对",
            "matchedTitle": override["sourceTitle"],
            "priceText": f"参考价 ¥{override['price']}",
            "priceBasis": "公开零售页面型号核对后的参考价",
            "updatedAt": UPDATED_AT,
            "note": "价格会随地区、版本和促销活动变化，下单前以支付入口展示为准。",
        }
        catalog.append(record)

    if len(catalog) < 40:
        raise RuntimeError(f"Only built {len(catalog)} products; expected at least 40")

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
