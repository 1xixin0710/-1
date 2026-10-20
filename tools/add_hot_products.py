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
        "name": "罗技 GPW4（小狗 / PRO 2 LIGHTSPEED）",
        "category": "desk",
        "category_label": "外设",
        "brand": "罗技",
        "price": 659,
        "compare_at": 1099,
        "stock": 36,
        "sales": 51800,
        "rating": 4.9,
        "review_count": 4821,
        "description": "GPW 四代轻量无线电竞鼠标，国内常称“小狗”，低延迟、长续航，适合 FPS 与高强度桌面使用。",
        "image_url": "https://2b.zol-img.com.cn/product/221_320x240/239/ceo7X21uBpig.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/mice/index1348608.shtml",
        "price_text": "ZOL 参考价 ¥1099；京东在售价 ¥659",
        "search_aliases": ["狗屁王", "GPW4小狗", "小狗"],
    },
    {
        "id": "desk-logitech-gpw5",
        "name": "罗技 GPW5（Ultra / PRO X2 SUPERSTRIKE）",
        "category": "desk",
        "category_label": "外设",
        "brand": "罗技",
        "price": 1349,
        "compare_at": 1979,
        "stock": 18,
        "sales": 28600,
        "rating": 4.9,
        "review_count": 1268,
        "description": "GPW 五代 Ultra 电竞鼠标，升级传感器与无线性能，面向高刷新率电竞配置。",
        "image_url": "https://2b.zol-img.com.cn/product/274_320x240/301/ceHJgzcCaKk.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/mice/index2158610.shtml",
        "price_text": "ZOL 参考价 ¥1979；近期京东活动价 ¥1349",
        "search_aliases": ["GPW5 Ultra", "GPW5雪豹", "雪豹"],
    },
    {
        "id": "desk-razer-viper-v3-pro",
        "name": "雷蛇 毒蝰 V3 Pro",
        "category": "desk",
        "category_label": "外设",
        "brand": "雷蛇",
        "price": 1299,
        "compare_at": 1599,
        "stock": 31,
        "sales": 47200,
        "rating": 4.8,
        "review_count": 2865,
        "description": "轻量化无线电竞鼠标，Focus Pro 35K 传感器与 8K 回报率，适合 FPS 和高速跟枪。",
        "image_url": "https://assets2.razerzone.com/images/pnx.assets/24970f67be4ba9644e28720377d91cfb/razer-viper-v3-pro-1200x630.webp",
        "source_name": "Razer 官方与国内公开报价",
        "source_url": "https://www.razer.com/gaming-mice/razer-viper-v3-pro",
        "price_text": "Razer 官方参考价 US$159.99；国内公开价约 ¥1299",
    },
    {
        "id": "desk-wooting-60he",
        "name": "Wooting 60HE V2 磁轴键盘",
        "category": "desk",
        "category_label": "外设",
        "brand": "Wooting",
        "price": 1599,
        "compare_at": 1899,
        "stock": 15,
        "sales": 32600,
        "rating": 4.9,
        "review_count": 1842,
        "description": "60% 配列模拟磁轴键盘，支持 Rapid Trigger、可调触发与网页驱动，面向竞技 FPS 玩家。",
        "image_url": "https://q9.itc.cn/q_70/images03/20250521/a18859c131214f308dd118b7f6bbf684.jpeg",
        "source_name": "Wooting 官方与公开评测",
        "source_url": "https://wooting.io/wooting-60he-v2",
        "price_text": "Wooting 官方参考价 US$175；国内公开价约 ¥1599",
    },
    {
        "id": "desk-iqunix-ev63",
        "name": "IQUNIX EV63 磁轴键盘",
        "category": "desk",
        "category_label": "外设",
        "brand": "IQUNIX",
        "price": 1349,
        "compare_at": None,
        "stock": 27,
        "sales": 43200,
        "rating": 4.9,
        "review_count": 3072,
        "description": "63 键铝合金磁轴键盘，支持 0.01mm Rapid Trigger、8K 回报率与网页驱动，轴体在详情页内选择。",
        "image_url": "https://cdn.shopify.com/s/files/1/0676/7853/5986/files/ev63-section2.jpg?v=12896019388382163290",
        "source_name": "IQUNIX 官方与 ZOL 国内报价",
        "source_url": "https://iqunix.com/products/iqunix-ev63-hall-effect-keyboard",
        "price_text": "IQUNIX 官方价 US$169-209；国内公开价 ¥1349-1549",
        "search_aliases": ["EV63磁轴", "IQUNIX EV63"],
        "colors": [
            {
                "name": "银武士",
                "value": "#c7c9c8",
                "image_url": "https://cdn.shopify.com/s/files/1/0676/7853/5986/files/ev63-section2.jpg?v=12896019388382163290",
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
                    {"id": "switch-magnetic-pro", "label": "磁玉轴 Pro", "priceDelta": 0},
                    {"id": "switch-x-pro", "label": "神秘X轴 Pro", "priceDelta": 100},
                    {"id": "switch-x-ultra", "label": "神秘X轴 Ultra", "priceDelta": 200},
                ],
            }
        ],
        "default_variant": {"switch": "switch-x-pro"},
    },
    {
        "id": "desk-rog-azoth-extreme",
        "name": "ROG 夜魔 Extreme 机械键盘",
        "category": "desk",
        "category_label": "外设",
        "brand": "ROG",
        "price": 3599,
        "compare_at": None,
        "stock": 9,
        "sales": 19600,
        "rating": 4.9,
        "review_count": 986,
        "description": "75% 铝合金三模客制化键盘，配 1.47 英寸 OLED 触控屏、可调 Gasket 结构和热插拔 ROG NX 轴。",
        "image_url": "https://dlcdnwebimgs.asus.com.cn/gain/A2AF9D47-DE84-4B81-8DD1-EF70766C67D1",
        "source_name": "ROG 中国官网",
        "source_url": "https://rog.asus.com.cn/keyboards/keyboards/compact/rog-azoth-extreme/",
        "price_text": "ROG 中国官网价 ¥3599",
        "search_aliases": ["夜魔Extreme", "ROG夜魔", "夜魔"],
        "variants": [
            {
                "id": "switch",
                "label": "轴体",
                "options": [
                    {"id": "switch-nx-snow", "label": "NX 雪武白轴", "priceDelta": 0},
                    {"id": "switch-nx-storm", "label": "NX 暴风蓝轴", "priceDelta": 0},
                ],
            }
        ],
        "default_variant": {"switch": "switch-nx-snow"},
    },
    {
        "id": "desk-logitech-g502x-plus",
        "name": "罗技 G502 X PLUS 无线游戏鼠标",
        "category": "desk",
        "category_label": "外设",
        "brand": "罗技",
        "price": 799,
        "compare_at": 1049,
        "stock": 42,
        "sales": 68400,
        "rating": 4.8,
        "review_count": 5362,
        "description": "G502 系列旗舰无线鼠标，搭载 HERO 25K 传感器、LIGHTFORCE 混合微动、13 个可编程按键与 LIGHTSYNC RGB。",
        "image_url": "https://2d.zol-img.com.cn/product/222_280x210/691/ceVVpjry9yu0U.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/mice/index1426842.shtml",
        "price_text": "ZOL 参考价 ¥1049；京东在售价 ¥799",
        "search_aliases": ["G502X Plus", "G502"],
    },
    {
        "id": "desk-mchose-g98-v3",
        "name": "迈从 G98 V3 机械键盘",
        "category": "desk",
        "category_label": "外设",
        "brand": "迈从",
        "price": 410,
        "compare_at": None,
        "stock": 38,
        "sales": 45800,
        "rating": 4.8,
        "review_count": 2148,
        "description": "98% 配列三模机械键盘，兼顾数字小键盘与桌面空间，适合办公、游戏和客制化入门。",
        "image_url": "https://2d.zol-img.com.cn/product/276_320x240/681/ceBRiHiPWbzo.png",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/keyboard/index2180689.shtml",
        "price_text": "ZOL 公开在售价 ¥410",
        "search_aliases": ["G98 V3", "迈从G98"],
    },
    {
        "id": "desk-aula-f75max",
        "name": "狼蛛 F75MAX 机械键盘",
        "category": "desk",
        "category_label": "外设",
        "brand": "狼蛛",
        "price": 349,
        "compare_at": None,
        "stock": 46,
        "sales": 57200,
        "rating": 4.7,
        "review_count": 3416,
        "description": "75% 配列三模热插拔键盘，主打 Gasket 结构和轻量化桌搭，星矢轴与收割者轴在同一商品内选择。",
        "image_url": "https://2b.zol-img.com.cn/product/276_698x437/51/cePZWimaAZZIs.png",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/keyboard/index2180491.shtml",
        "price_text": "ZOL 公开在售价 ¥349 起",
        "search_aliases": ["F75 MAX", "狼蛛F75"],
        "variants": [
            {
                "id": "switch",
                "label": "轴体",
                "options": [
                    {"id": "switch-star-arrow", "label": "星矢轴", "priceDelta": 0},
                    {"id": "switch-harvester", "label": "收割者轴", "priceDelta": 20},
                ],
            }
        ],
        "default_variant": {"switch": "switch-star-arrow"},
    },
    {
        "id": "desk-madcatz-mad75",
        "name": "美加狮 MAD 75 机械键盘",
        "category": "desk",
        "category_label": "外设",
        "brand": "美加狮",
        "price": 289,
        "compare_at": None,
        "stock": 34,
        "sales": 28300,
        "rating": 4.7,
        "review_count": 1276,
        "description": "75% 配列三模机械键盘，紧凑布局、热插拔与 Gasket 结构兼顾游戏和日常输入。",
        "image_url": "https://2e.zol-img.com.cn/product/276_320x240/24/ceqj6xnZpBINA.png",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/keyboard/index2180478.shtml",
        "price_text": "ZOL 公开在售价 ¥289",
        "search_aliases": ["MAD75", "美加狮MAD75"],
    },
    {
        "id": "desk-logitech-g304x",
        "name": "罗技 G304X 无线游戏鼠标",
        "category": "desk",
        "category_label": "外设",
        "brand": "罗技",
        "price": 199,
        "compare_at": 209,
        "stock": 58,
        "sales": 91600,
        "rating": 4.8,
        "review_count": 8824,
        "description": "罗技入门无线游戏鼠标，HERO 传感器、长续航与轻巧机身，适合学生党和首次搭建电竞桌面。",
        "image_url": "https://2c.zol-img.com.cn/product/275_320x240/740/ceIJ6re0ZbiI.png",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/mice/index2162390.shtml",
        "price_text": "ZOL 参考价 ¥209；京东在售价 ¥199",
        "search_aliases": ["G304", "罗技G304X"],
    },
    {
        "id": "desk-rapoo-vt9-max",
        "name": "雷柏 VT9 MAX 二代双 8K 无线鼠标",
        "category": "desk",
        "category_label": "外设",
        "brand": "雷柏",
        "price": 329,
        "compare_at": None,
        "stock": 44,
        "sales": 62300,
        "rating": 4.8,
        "review_count": 4186,
        "description": "国产高性价比无线电竞鼠标，双 8K 回报率、轻量化机身与长续航，适合 FPS 玩家和桌面主力鼠标。",
        "image_url": "https://2b.zol-img.com.cn/product/274_320x240/861/ce6BPPeO28ak.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/mice/index2149947.shtml",
        "price_text": "ZOL 公开参考价 ¥329",
        "search_aliases": ["VT9 MAX", "VT9MAX", "雷柏VT9"],
    },
    {
        "id": "desk-rapoo-vt3s-max",
        "name": "雷柏 VT3s MAX 无线游戏鼠标",
        "category": "desk",
        "category_label": "外设",
        "brand": "雷柏",
        "price": 299,
        "compare_at": None,
        "stock": 39,
        "sales": 38600,
        "rating": 4.8,
        "review_count": 2294,
        "description": "轻量化右手无线电竞鼠标，兼顾抓握与趴握，适合中大手型玩家和主流 2K、4K 电竞桌面。",
        "image_url": "https://2e.zol-img.com.cn/product/275_320x240/538/ceaDej8xT6A6.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/mice/index2169495.shtml",
        "price_text": "ZOL 公开参考价 ¥299",
        "search_aliases": ["VT3s MAX", "雷柏VT3s"],
    },
    {
        "id": "desk-logitech-mx-master-4",
        "name": "罗技 MX Master 4 无线鼠标",
        "category": "desk",
        "category_label": "外设",
        "brand": "罗技",
        "price": 899,
        "compare_at": None,
        "stock": 26,
        "sales": 27700,
        "rating": 4.8,
        "review_count": 1893,
        "description": "旗舰办公无线鼠标，主打多设备切换、精细滚轮与人体工学握持，适合创作、办公和跨平台使用。",
        "image_url": "https://2d.zol-img.com.cn/product/274_320x240/811/ce1P8QyRCiCg.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/mice/index2153839.shtml",
        "price_text": "ZOL 公开参考价 ¥899",
        "search_aliases": ["MX Master4", "MX Master 4"],
    },
    {
        "id": "desk-flydigi-icewolf",
        "name": "飞智 冰原狼 多模版游戏手柄",
        "category": "desk",
        "category_label": "外设",
        "brand": "飞智",
        "price": 199,
        "compare_at": None,
        "stock": 61,
        "sales": 54800,
        "rating": 4.7,
        "review_count": 3618,
        "description": "国产多模游戏手柄，支持 PC、手机与 Switch，霍尔摇杆和体感操控适合学生党与跨平台玩家。",
        "image_url": "https://2a.zol-img.com.cn/product/226_320x240/226/cewi7bUmaph2Q.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/gamepad/index1439959.shtml",
        "price_text": "ZOL 公开参考价 ¥199",
        "search_aliases": ["冰原狼", "飞智手柄"],
    },
    {
        "id": "desk-beitong-kunpeng-50",
        "name": "北通 鲲鹏 50 智能游戏手柄",
        "category": "desk",
        "category_label": "外设",
        "brand": "北通",
        "price": 369,
        "compare_at": None,
        "stock": 35,
        "sales": 41200,
        "rating": 4.8,
        "review_count": 2645,
        "description": "面向 PC 和主机的智能游戏手柄，支持自定义按键、体感与多平台连接，适合动作和竞速游戏。",
        "image_url": "https://2b.zol-img.com.cn/product/270_280x210/23/cevrjBotGz4SI.png",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/gamepad/index2113841.shtml",
        "price_text": "ZOL 公开参考价 ¥369",
        "search_aliases": ["鲲鹏50", "北通手柄"],
    },
    {
        "id": "desk-8bitdo-orion-wireless",
        "name": "八位堂 猎户座真无线手柄 十周年国内共创版",
        "category": "desk",
        "category_label": "外设",
        "brand": "八位堂",
        "price": 458,
        "compare_at": None,
        "stock": 23,
        "sales": 24600,
        "rating": 4.8,
        "review_count": 1572,
        "description": "八位堂猎户座十周年国内共创版，支持 PC、Switch 与移动设备，兼顾霍尔摇杆、体感和复古外观。",
        "image_url": "https://2c.zol-img.com.cn/product/249_698x437/292/ce23Z7yezF1bA.jpg",
        "source_name": "ZOL 中关村在线",
        "source_url": "https://detail.zol.com.cn/gamepad/index1827284.shtml",
        "price_text": "ZOL 公开参考价 ¥458",
        "search_aliases": ["八位堂猎户座", "猎户座手柄"],
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

REMOVED_MARKET_IDS = {
    "desk-market-2181204",
    "desk-market-2180780",
    "desk-market-2180756",
    "desk-market-2180753",
    "desk-market-2180752",
    "desk-market-2180750",
    "desk-market-2180749",
    "desk-market-2180816",
    "desk-market-2180815",
    "desk-market-2180810",
    "desk-market-2178341",
    "desk-market-2178340",
    "desk-market-2178338",
    "desk-market-2178337",
    "audio-market-2169631",
    "audio-market-2109554",
    "audio-market-69156",
    "audio-market-69159",
    "audio-market-1166385",
    "audio-market-2180006",
    "audio-market-2180011",
    "audio-market-2158948",
    "audio-market-2131584",
    "audio-market-2123273",
    "audio-market-2123270",
}


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
        "searchAliases": spec.get("search_aliases") or [],
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


def normalize_category_labels(catalog: list[dict]) -> list[dict]:
    for product in catalog:
        if product["category"] == "desk":
            product["categoryLabel"] = "外设"
            product["series"] = str(product.get("series") or "").replace(
                "桌面办公", "外设"
            )
    return catalog


def main() -> None:
    catalog_path = DATA_DIR / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    catalog = enrich_catalog(catalog)
    catalog = [
        product for product in catalog if product["id"] not in REMOVED_MARKET_IDS
    ]
    catalog = merge_f87_switch_variants(catalog)

    hot_ids = {spec["id"] for spec in HOT_PRODUCTS}
    catalog = [product for product in catalog if product["id"] not in hot_ids]
    additions = [build_product(spec) for spec in HOT_PRODUCTS]
    catalog = normalize_category_labels(additions + catalog)

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
