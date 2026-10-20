from __future__ import annotations

import json
from pathlib import Path

from augment_market_catalog import save_image
from catalog_variants import enrich_catalog


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
MARKET_IMAGE_DIR = ROOT / "assets" / "market"
UPDATED_AT = "2026-10-20"

HOT_PRODUCTS = [
    {
        "id": "desk-logitech-gpw",
        "name": "罗技 G PRO X SUPERLIGHT（GPW）",
        "category": "desk",
        "category_label": "桌面办公",
        "brand": "罗技",
        "price": 659,
        "compare_at": 1099,
        "stock": 36,
        "sales": 51800,
        "rating": 4.9,
        "review_count": 4821,
        "description": "GPW 系列经典轻量无线电竞鼠标，低延迟、长续航，适合 FPS 与日常桌面使用。",
        "image_url": "https://2b.zol-img.com.cn/product/221_320x240/239/ceo7X21uBpig.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/mice/index1348608.shtml",
        "price_text": "ZOL 参考价 ¥1099；京东在售价 ¥659",
    },
    {
        "id": "desk-logitech-gpw5",
        "name": "罗技 GPW 5 雪豹（PRO X2 SUPERSTRIKE）",
        "category": "desk",
        "category_label": "桌面办公",
        "brand": "罗技",
        "price": 1349,
        "compare_at": 1979,
        "stock": 18,
        "sales": 28600,
        "rating": 4.9,
        "review_count": 1268,
        "description": "GPW 第五代雪豹电竞鼠标，升级传感器与无线性能，面向高刷新率电竞桌面。",
        "image_url": "https://2b.zol-img.com.cn/product/274_320x240/301/ceHJgzcCaKk.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/mice/index2158610.shtml",
        "price_text": "ZOL 参考价 ¥1979；近期京东活动价 ¥1349",
    },
    {
        "id": "desk-iqunix-ev63",
        "name": "IQUNIX EV63 磁轴机械键盘",
        "category": "desk",
        "category_label": "桌面办公",
        "brand": "IQUNIX",
        "price": 1189,
        "compare_at": 1399,
        "stock": 27,
        "sales": 43200,
        "rating": 4.9,
        "review_count": 3072,
        "description": "63 键铝合金磁轴键盘，支持 0.01mm Rapid Trigger、8K 回报率与网页驱动，轴体在详情页内选择。",
        "image_url": "https://cdn.shopify.com/s/files/1/0676/7853/5986/files/EV63_Silver_Knight_with_Magnetic_X_Ultra_Switch.png?v=1781340006",
        "source_name": "IQUNIX 官方与 ZOL 公开报价",
        "source_url": "https://iqunix.com/products/iqunix-ev63-hall-effect-keyboard",
        "price_text": "ZOL 参考价 ¥1249-1549；近期京东活动价约 ¥1189",
        "colors": [
            {
                "name": "银武士",
                "value": "#c7c9c8",
                "image_url": "https://cdn.shopify.com/s/files/1/0676/7853/5986/files/EV63_Silver_Knight_with_Magnetic_X_Ultra_Switch.png?v=1781340006",
            },
            {
                "name": "紫罗兰",
                "value": "#8b78aa",
                "image_url": "https://cdn.shopify.com/s/files/1/0676/7853/5986/files/04_ee0aad70-2530-4881-9fab-5e08f198c0cf.jpg?v=1765951802",
            },
            {
                "name": "黑武士",
                "value": "#26272b",
                "image_url": "https://cdn.shopify.com/s/files/1/0676/7853/5986/files/iQunix_EV63_-2.jpg?v=1765961799",
            },
        ],
        "variants": [
            {
                "id": "switch",
                "label": "轴体",
                "options": [
                    {"id": "switch-magnetic-pro", "label": "磁玉轴 Pro", "priceDelta": -100},
                    {"id": "switch-x-pro", "label": "神秘X轴 Pro", "priceDelta": 0},
                    {"id": "switch-x-ultra", "label": "神秘X轴 Ultra", "priceDelta": 200},
                ],
            }
        ],
        "default_variant": {"switch": "switch-x-pro"},
    },
    {
        "id": "tablet-xiaomi-pad7-ultra",
        "name": "小米平板7 Ultra（12GB/256GB）",
        "category": "tablet",
        "category_label": "平板电脑",
        "brand": "小米",
        "price": 5199,
        "compare_at": 5699,
        "stock": 24,
        "sales": 36700,
        "rating": 4.8,
        "review_count": 2146,
        "description": "14 英寸 3.2K 高刷大屏，玄戒 O1 处理器与 120W 快充，兼顾影音、办公和轻创作。",
        "image_url": "https://2f.zol-img.com.cn/product/272_320x240/801/ceevo6ruI14rY.png",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/tablepc/index2128636.shtml",
        "price_text": "ZOL 参考价 ¥5699；京东在售价 ¥5199",
        "variants": [
            {
                "id": "storage",
                "label": "存储容量",
                "options": [
                    {"id": "storage-256gb", "label": "256GB", "priceDelta": 0},
                    {"id": "storage-512gb", "label": "512GB", "priceDelta": 300},
                    {"id": "storage-1tb", "label": "1TB", "priceDelta": 1700},
                ],
            }
        ],
        "default_variant": {"storage": "storage-256gb"},
    },
    {
        "id": "computer-legion-y9000p-2025",
        "name": "联想拯救者Y9000P 2025 AI元启（Ultra 9/32GB/1TB/RTX5060）",
        "category": "computer",
        "category_label": "电脑办公",
        "brand": "联想",
        "price": 11999,
        "compare_at": None,
        "stock": 12,
        "sales": 23900,
        "rating": 4.8,
        "review_count": 1687,
        "description": "2025 款高性能游戏本，Ultra 9 处理器、32GB 内存、1TB 固态与 RTX 5060 独立显卡。",
        "image_url": "https://2e.zol-img.com.cn/product/272_320x240/438/ceF1EgXZEwUpU.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/notebook/index2128701.shtml",
        "price_text": "ZOL 公开参考价 ¥11999",
        "variants": [],
    },
    {
        "id": "camera-dji-action5-pro",
        "name": "大疆 Osmo Action 5 Pro 标准套装",
        "category": "camera",
        "category_label": "摄影器材",
        "brand": "大疆",
        "price": 2598,
        "compare_at": None,
        "stock": 21,
        "sales": 31100,
        "rating": 4.8,
        "review_count": 1934,
        "description": "旗舰运动相机标准套装，支持高动态范围视频、超强防抖与裸机防水，适合旅行和户外记录。",
        "image_url": "https://2a.zol-img.com.cn/product/269_320x240/348/cecwifdSnVqU.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/Action_camera/index2106423.shtml",
        "price_text": "ZOL 公开参考价 ¥2598",
    },
    {
        "id": "audio-airpods-pro-3",
        "name": "苹果 AirPods Pro 3",
        "category": "audio",
        "category_label": "耳机影音",
        "brand": "苹果",
        "price": 1839,
        "compare_at": None,
        "stock": 42,
        "sales": 62400,
        "rating": 4.8,
        "review_count": 5218,
        "description": "苹果主动降噪真无线耳机，空间音频、通透模式与多设备切换体验完整。",
        "image_url": "https://2a.zol-img.com.cn/product/273_320x240/518/ceiJ3mmwB4iO6.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/microphone/index1794828.shtml",
        "price_text": "ZOL 公开参考价 ¥1839",
    },
    {
        "id": "audio-huawei-freebuds-pro5",
        "name": "华为 FreeBuds Pro 5 悦彰耳机",
        "category": "audio",
        "category_label": "耳机影音",
        "brand": "华为",
        "price": 1349,
        "compare_at": None,
        "stock": 33,
        "sales": 45300,
        "rating": 4.8,
        "review_count": 2864,
        "description": "华为旗舰降噪真无线耳机，兼顾通勤降噪、清晰通话与高解析音频。",
        "image_url": "https://2e.zol-img.com.cn/product/274_320x240/566/ceT5TGCM9H8dA.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/microphone/index2148490.shtml",
        "price_text": "ZOL 公开参考价 ¥1349",
    },
    {
        "id": "audio-sony-wh1000xm5",
        "name": "索尼 WH-1000XM5 头戴式降噪耳机",
        "category": "audio",
        "category_label": "耳机影音",
        "brand": "索尼",
        "price": 2999,
        "compare_at": None,
        "stock": 16,
        "sales": 39700,
        "rating": 4.8,
        "review_count": 3561,
        "description": "索尼旗舰头戴式降噪耳机，适合长途通勤、飞行与专注办公。",
        "image_url": "https://2a.zol-img.com.cn/product/219_320x240/688/ceEE1WD7Z3bs.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/microphone/index1408101.shtml",
        "price_text": "ZOL 公开参考价 ¥2999",
    },
    {
        "id": "audio-huawei-freeclip2",
        "name": "华为 FreeClip 2 耳夹耳机",
        "category": "audio",
        "category_label": "耳机影音",
        "brand": "华为",
        "price": 1299,
        "compare_at": None,
        "stock": 29,
        "sales": 41900,
        "rating": 4.8,
        "review_count": 2473,
        "description": "开放式耳夹设计，佩戴轻巧透气，适合长时间办公、运动与日常通勤。",
        "image_url": "https://2e.zol-img.com.cn/product/273_320x240/804/ce3qmCfgFOCV2.png",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/microphone/index2143087.shtml",
        "price_text": "ZOL 公开参考价 ¥1299",
    },
]


def gallery(source: str) -> list[dict]:
    return [
        {
            "src": source,
            "position": "50% 50%",
            "scale": 1,
            "fit": "contain",
            "filter": "none",
        }
    ]


def save_product_image(slug: str, image_url: str, suffix: str = "") -> str:
    destination = MARKET_IMAGE_DIR / f"hot-{slug}{suffix}.jpg"
    if not destination.exists() and not save_image(image_url, destination):
        raise RuntimeError(f"Could not save image for {slug}: {image_url}")
    return f"./{destination.relative_to(ROOT).as_posix()}"


def build_product(spec: dict) -> dict:
    main_image = save_product_image(spec["id"], spec["image_url"])
    color_specs = spec.get("colors") or [
        {"name": "标准配色", "value": "#696d70", "image_url": spec["image_url"]}
    ]
    colors = []
    for index, color in enumerate(color_specs):
        image_path = (
            main_image
            if index == 0
            else save_product_image(spec["id"], color["image_url"], f"-{index}")
        )
        colors.append(
            {
                "name": color["name"],
                "value": color["value"],
                "gallery": gallery(image_path),
            }
        )

    return {
        "id": spec["id"],
        "name": spec["name"],
        "displayName": spec["name"],
        "series": f"{spec['category_label']} / 热门精选",
        "category": spec["category"],
        "categoryLabel": spec["category_label"],
        "brand": spec["brand"],
        "price": spec["price"],
        "priceLabel": f"¥{spec['price']}",
        "compareAt": spec.get("compare_at"),
        "stock": spec["stock"],
        "sales": spec["sales"],
        "rating": spec["rating"],
        "reviewCount": spec["review_count"],
        "featured": True,
        "description": spec["description"],
        "materials": "官方公开配置，具体版本、包装和参数以商品页及订单确认页为准。",
        "delivery": "现货商品预计 1 至 3 日送达，大件商品按地区预约配送。",
        "image": main_image,
        "colors": colors,
        "variantGroups": spec.get("variants") or [],
        "defaultVariant": spec.get("default_variant") or {},
        "source": {
            "name": spec["source_name"],
            "url": spec["source_url"],
            "listUrl": spec["source_url"],
            "matchedTitle": spec["name"],
            "priceText": spec["price_text"],
            "priceBasis": "公开在售价与参考价作为基准，页面在此基础上展示小幅行情波动",
            "updatedAt": UPDATED_AT,
            "note": "价格随地区、版本和促销活动变化；支付入口仅作演示。",
        },
    }


def merge_f87_switch_variants(catalog: list[dict]) -> list[dict]:
    first_id = "desk-market-2181205"
    second_id = "desk-market-2181204"
    first = next((product for product in catalog if product["id"] == first_id), None)
    if first is None:
        return catalog

    first["name"] = "狼蛛F87Pro V2宗师版"
    first["displayName"] = "狼蛛F87Pro V2宗师版"
    first["brand"] = "狼蛛"
    first["description"] = (
        "87 键热插拔机械键盘，海穹轴与焦糖拿铁轴在同一商品内选择，不再拆成重复商品卡。"
    )
    first["variantGroups"] = [
        {
            "id": "switch",
            "label": "轴体",
            "options": [
                {"id": "switch-haiqiong", "label": "海穹轴", "priceDelta": 0},
                {
                    "id": "switch-caramel-latte",
                    "label": "焦糖拿铁轴",
                    "priceDelta": -12,
                },
            ],
        }
    ]
    first["defaultVariant"] = {"switch": "switch-haiqiong"}
    return [product for product in catalog if product["id"] != second_id]


def main() -> None:
    catalog_path = DATA_DIR / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog = enrich_catalog(catalog)
    catalog = merge_f87_switch_variants(catalog)

    hot_ids = {spec["id"] for spec in HOT_PRODUCTS}
    catalog = [product for product in catalog if product["id"] not in hot_ids]
    additions = [build_product(spec) for spec in HOT_PRODUCTS]
    catalog = additions + catalog

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
    print(f"Wrote {len(catalog)} products with {len(additions)} new hot picks")


if __name__ == "__main__":
    main()
