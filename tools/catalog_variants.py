from __future__ import annotations

import re

PHONE_MEMORY_PRICES = {
    12: 0,
    16: 900,
}

COMPUTER_MEMORY_PRICES = {
    8: 0,
    16: 600,
    24: 1400,
    32: 2200,
    64: 5000,
}

PHONE_STORAGE_PRICES = {
    128: 0,
    256: 0,
    512: 1000,
    1024: 3000,
    2048: 6000,
}

COMPUTER_STORAGE_PRICES = {
    256: 0,
    512: 500,
    1024: 1200,
    2048: 3200,
    4096: 6500,
}

PHONE_COLORS = [
    {"name": "曜石黑", "value": "#20242b", "filter": "none"},
    {
        "name": "云雾白",
        "value": "#e8e7e2",
        "filter": "brightness(1.17) saturate(.56) contrast(.94)",
    },
    {
        "name": "钛金灰",
        "value": "#8d8a84",
        "filter": "sepia(.28) grayscale(.12) brightness(1.06) contrast(.96)",
    },
    {
        "name": "冰川蓝",
        "value": "#8faec7",
        "filter": "sepia(.42) hue-rotate(155deg) saturate(1.9) brightness(1.02)",
    },
    {
        "name": "晨曦金",
        "value": "#d4b17a",
        "filter": "sepia(.58) saturate(1.25) brightness(1.08)",
    },
    {
        "name": "松林绿",
        "value": "#496252",
        "filter": "sepia(.36) hue-rotate(72deg) saturate(1.55) brightness(.96)",
    },
]

COMPUTER_COLORS = [
    {"name": "深空灰", "value": "#4d5157", "filter": "none"},
    {
        "name": "月光银",
        "value": "#c8cacc",
        "filter": "brightness(1.15) saturate(.5) contrast(.94)",
    },
    {
        "name": "午夜色",
        "value": "#293346",
        "filter": "sepia(.25) hue-rotate(180deg) saturate(1.2) brightness(.82)",
    },
    {
        "name": "星光色",
        "value": "#e7dfcf",
        "filter": "sepia(.12) brightness(1.16) saturate(.7)",
    },
    {
        "name": "天空蓝",
        "value": "#9ab7d1",
        "filter": "sepia(.45) hue-rotate(160deg) saturate(1.8)",
    },
    {
        "name": "玫瑰金",
        "value": "#c6a29c",
        "filter": "sepia(.48) hue-rotate(310deg) saturate(1.25) brightness(1.03)",
    },
]

CAMERA_COLORS = [
    {"name": "经典黑", "value": "#17191d", "filter": "none"},
    {
        "name": "银黑",
        "value": "#a8aaae",
        "filter": "grayscale(.42) brightness(1.16) contrast(.94)",
    },
    {
        "name": "石墨灰",
        "value": "#565b60",
        "filter": "grayscale(.2) brightness(.92) contrast(1.08)",
    },
    {
        "name": "钛金属",
        "value": "#8f8d88",
        "filter": "sepia(.24) brightness(1.08) contrast(.96)",
    },
    {
        "name": "森林绿",
        "value": "#40594a",
        "filter": "sepia(.32) hue-rotate(76deg) saturate(1.55) brightness(.94)",
    },
    {
        "name": "午夜蓝",
        "value": "#273a53",
        "filter": "sepia(.38) hue-rotate(170deg) saturate(1.55) brightness(.88)",
    },
]

APPLIANCE_COLORS = [
    {"name": "云白", "value": "#ecece7", "filter": "brightness(1.16) saturate(.58)"},
    {
        "name": "钛灰",
        "value": "#737a7e",
        "filter": "grayscale(.35) brightness(.98) contrast(1.02)",
    },
    {
        "name": "曜石黑",
        "value": "#23272c",
        "filter": "brightness(.78) saturate(.55) contrast(1.08)",
    },
    {
        "name": "海盐蓝",
        "value": "#8ba7b8",
        "filter": "sepia(.35) hue-rotate(155deg) saturate(1.65) brightness(1.02)",
    },
    {
        "name": "燕麦米",
        "value": "#d7c9ac",
        "filter": "sepia(.38) saturate(.9) brightness(1.08)",
    },
    {
        "name": "鼠尾草绿",
        "value": "#879786",
        "filter": "sepia(.3) hue-rotate(75deg) saturate(1.35) brightness(.99)",
    },
]

COLOR_SETS = {
    "phone": PHONE_COLORS,
    "computer": COMPUTER_COLORS,
    "camera": CAMERA_COLORS,
    "appliance": APPLIANCE_COLORS,
}

IPHONE_18_PRO_GALLERY = [
    {
        "name": "勃艮第酒红色",
        "value": "#5a2636",
        "gallery": [
            {
                "src": "./assets/catalog/iphone-18-pro-burgundy.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "cover",
            },
            {
                "src": "./assets/catalog/iphone-18-pro-camera-control.jpg",
                "position": "66% 44%",
                "scale": 1.08,
                "fit": "cover",
            },
            {
                "src": "./assets/catalog/iphone-18-pro-main-camera.jpg",
                "position": "48% 48%",
                "scale": 1,
                "fit": "cover",
            },
        ],
    },
    {
        "name": "冰川蓝",
        "value": "#9eb6c9",
        "gallery": [
            {
                "src": "./assets/catalog/iphone-18-pro-glacier.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "cover",
            },
            {
                "src": "./assets/catalog/iphone-18-pro-camera-control.jpg",
                "position": "66% 44%",
                "scale": 1.08,
                "fit": "cover",
            },
            {
                "src": "./assets/catalog/iphone-18-pro-main-camera.jpg",
                "position": "48% 48%",
                "scale": 1,
                "fit": "cover",
            },
        ],
    },
    {
        "name": "银色",
        "value": "#d8d8d5",
        "gallery": [
            {
                "src": "./assets/catalog/iphone-18-pro-silver.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "cover",
            },
            {
                "src": "./assets/catalog/iphone-18-pro-camera-control.jpg",
                "position": "66% 44%",
                "scale": 1.08,
                "fit": "cover",
            },
            {
                "src": "./assets/catalog/iphone-18-pro-main-camera.jpg",
                "position": "48% 48%",
                "scale": 1,
                "fit": "cover",
            },
        ],
    },
    {
        "name": "黑色",
        "value": "#242527",
        "gallery": [
            {
                "src": "./assets/catalog/iphone-18-pro-black.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "cover",
            },
            {
                "src": "./assets/catalog/iphone-18-pro-camera-control.jpg",
                "position": "66% 44%",
                "scale": 1.08,
                "fit": "cover",
            },
            {
                "src": "./assets/catalog/iphone-18-pro-main-camera.jpg",
                "position": "48% 48%",
                "scale": 1,
                "fit": "cover",
            },
        ],
    },
]

MACBOOK_AIR_GALLERY = [
    {
        "name": "天空蓝",
        "value": "#9ab7d1",
        "gallery": [
            {
                "src": "./assets/catalog/macbook-air-skyblue-top.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "contain",
            },
            {
                "src": "./assets/catalog/macbook-air-skyblue-side.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "contain",
            },
        ],
    },
    {
        "name": "银色",
        "value": "#d5d7d8",
        "gallery": [
            {
                "src": "./assets/catalog/macbook-air-silver-top.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "contain",
            },
            {
                "src": "./assets/catalog/macbook-air-silver-side.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "contain",
            },
        ],
    },
    {
        "name": "星光色",
        "value": "#e6ddca",
        "gallery": [
            {
                "src": "./assets/catalog/macbook-air-starlight-top.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "contain",
            },
            {
                "src": "./assets/catalog/macbook-air-starlight-side.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "contain",
            },
        ],
    },
    {
        "name": "午夜色",
        "value": "#263247",
        "gallery": [
            {
                "src": "./assets/catalog/macbook-air-midnight-top.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "contain",
            },
            {
                "src": "./assets/catalog/macbook-air-midnight-side.jpg",
                "position": "50% 50%",
                "scale": 1,
                "fit": "contain",
            },
        ],
    },
]

COLOR_GALLERY_OVERRIDES = {
    "phone-anchor-2177308": IPHONE_18_PRO_GALLERY,
    "phone-009-2177461": IPHONE_18_PRO_GALLERY,
    "computer-apple-macbook-air-m4": MACBOOK_AIR_GALLERY,
}


def size_label(value: int) -> str:
    if value >= 1024 and value % 1024 == 0:
        return f"{value // 1024}TB"
    return f"{value}GB"


def option_id(prefix: str, value: int) -> str:
    return f"{prefix}-{size_label(value).lower()}"


def parse_capacity_specs(name: str) -> list[int]:
    values: list[int] = []
    for number, unit in re.findall(r"(\d+)\s*(GB|TB)", name, flags=re.IGNORECASE):
        value = int(number) * (1024 if unit.upper() == "TB" else 1)
        if value not in values:
            values.append(value)
    return values


def infer_base_specs(product: dict) -> tuple[int, int]:
    category = product.get("category")
    values = parse_capacity_specs(str(product.get("name") or ""))
    defaults = (12, 256) if category == "phone" else (16, 512)
    memory = next((value for value in values if value <= 64), defaults[0])
    storage = next(
        (value for value in reversed(values) if value >= 128 and value != memory),
        defaults[1],
    )
    return memory, storage


def memory_options(category: str, base_memory: int) -> list[int]:
    if category == "phone":
        values = {12, 16, base_memory}
        return sorted(values)
    if base_memory <= 16:
        values = {16, 32, base_memory}
    elif base_memory <= 24:
        values = {16, 24, 32}
    else:
        values = {16, 32, 64, base_memory}
    return sorted(values)


def storage_options(category: str, base_storage: int) -> list[int]:
    if category == "phone":
        if base_storage <= 128:
            values = {128, 256, 512}
        elif base_storage <= 256:
            values = {256, 512, 1024}
        elif base_storage <= 512:
            values = {256, 512, 1024}
        else:
            values = {512, 1024, 2048}
        values.add(base_storage)
        return sorted(values)

    if base_storage <= 256:
        values = {256, 512, 1024}
    elif base_storage <= 512:
        values = {512, 1024, 2048}
    elif base_storage <= 1024:
        values = {512, 1024, 2048}
    else:
        values = {1024, 2048, 4096}
    values.add(base_storage)
    return sorted(values)


def build_variant_groups(product: dict) -> tuple[list[dict], dict[str, str], str]:
    category = product.get("category")
    base_memory, base_storage = infer_base_specs(product)

    if category == "phone":
        memory_prices = PHONE_MEMORY_PRICES
        storage_prices = PHONE_STORAGE_PRICES
        memory_label = "运行内存"
        storage_label = "存储容量"
    elif category == "computer":
        memory_prices = COMPUTER_MEMORY_PRICES
        storage_prices = COMPUTER_STORAGE_PRICES
        memory_label = "内存"
        storage_label = "硬盘容量"
    else:
        return [], {}, str(product.get("name") or "")

    base_memory_price = memory_prices.get(base_memory, 0)
    base_storage_price = storage_prices.get(base_storage, 0)
    memory_group = {
        "id": "memory",
        "label": memory_label,
        "options": [
            {
                "id": option_id("memory", value),
                "label": size_label(value),
                "priceDelta": memory_prices.get(value, 0) - base_memory_price,
            }
            for value in memory_options(category, base_memory)
        ],
    }
    storage_group = {
        "id": "storage",
        "label": storage_label,
        "options": [
            {
                "id": option_id("storage", value),
                "label": size_label(value),
                "priceDelta": storage_prices.get(value, 0) - base_storage_price,
            }
            for value in storage_options(category, base_storage)
        ],
    }
    default_variant = {
        "memory": memory_group["options"][
            next(
                index
                for index, option in enumerate(memory_group["options"])
                if option["label"] == size_label(base_memory)
            )
        ]["id"],
        "storage": storage_group["options"][
            next(
                index
                for index, option in enumerate(storage_group["options"])
                if option["label"] == size_label(base_storage)
            )
        ]["id"],
    }
    display_name = re.sub(
        r"\s*[\(（][^)）]*(?:\d+\s*(?:GB|TB)[^)）]*)[\)）]",
        "",
        str(product.get("name") or ""),
        flags=re.IGNORECASE,
    ).strip()
    return [memory_group, storage_group], default_variant, display_name or product["name"]


def gallery_view(
    source: str,
    position: str,
    scale: float,
    filter_value: str,
) -> dict:
    return {
        "src": source,
        "position": position,
        "scale": scale,
        "fit": "cover",
        "filter": filter_value,
    }


def build_color_gallery(product: dict, color: dict) -> list[dict]:
    source = str(color.get("image") or product.get("image") or "")
    filter_value = str(color.get("filter") or "none")
    return [
        gallery_view(source, "50% 50%", 1, filter_value),
        gallery_view(source, "54% 72%", 1.28, filter_value),
        gallery_view(source, "43% 38%", 1.52, filter_value),
    ]


def enrich_colors(product: dict) -> None:
    override = COLOR_GALLERY_OVERRIDES.get(str(product.get("id") or ""))
    if override:
        product["colors"] = [
            {
                **{key: value for key, value in color.items() if key != "gallery"},
                "gallery": [dict(item) for item in color["gallery"]],
            }
            for color in override
        ]
        return

    current = product.get("colors")
    if isinstance(current, list) and len(current) >= 4 and all(
        isinstance(color, dict) and color.get("gallery") for color in current
    ):
        return

    palette = COLOR_SETS.get(str(product.get("category") or ""), [])
    if not palette:
        return

    product["colors"] = [
        {
            **dict(color),
            "gallery": build_color_gallery(product, color),
        }
        for color in palette
    ]


def enrich_catalog(catalog: list[dict]) -> list[dict]:
    for product in catalog:
        enrich_colors(product)
        variant_groups, default_variant, display_name = build_variant_groups(product)
        if not variant_groups:
            product.pop("variantGroups", None)
            product.pop("defaultVariant", None)
            product.pop("displayName", None)
            continue
        product["variantGroups"] = variant_groups
        product["defaultVariant"] = default_variant
        product["displayName"] = display_name
    return catalog
