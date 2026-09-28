from __future__ import annotations

import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
IMAGE_DIR = ROOT / "assets" / "catalog"
UPDATED_AT = "2026-09-28"

CATEGORY_LABELS = {
    "phone": "手机数码",
    "computer": "电脑办公",
    "camera": "摄影器材",
    "appliance": "家用电器",
}

COLOR_SETS = {
    "phone": [
        {"name": "曜石黑", "value": "#20242b"},
        {"name": "云杉白", "value": "#e8e7e2"},
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

PRODUCTS = [
    {
        "id": "phone-apple-iphone-16-pro-max",
        "query": "iPhone 16 Pro Max 256GB",
        "name": "Apple iPhone 16 Pro Max 256GB",
        "brand": "苹果",
        "category": "phone",
        "price": 9999,
        "compareAt": 10999,
        "description": "A18 Pro 芯片、钛金属机身与 5 倍长焦组合，适合重视影像和长期系统体验的用户。",
        "specs": "6.9 英寸超视网膜 XDR、A18 Pro、256GB、5 倍长焦",
    },
    {
        "id": "phone-huawei-mate-70-pro",
        "query": "华为 Mate 70 Pro",
        "name": "HUAWEI Mate 70 Pro 12GB+512GB",
        "brand": "华为",
        "category": "phone",
        "price": 6999,
        "compareAt": 7499,
        "description": "面向商务和影像用户的旗舰机型，鸿蒙生态、卫星通信和长续航是主要卖点。",
        "specs": "12GB+512GB、鸿蒙系统、卫星通信、旗舰影像",
    },
    {
        "id": "phone-xiaomi-15-ultra",
        "query": "小米 15 Ultra 256GB",
        "name": "小米 15 Ultra 12GB+256GB",
        "brand": "小米",
        "category": "phone",
        "price": 6499,
        "compareAt": 6999,
        "description": "徕卡影像系统与一英寸主摄组合，兼顾高性能游戏和专业摄影。",
        "specs": "徕卡一英寸主摄、2 亿长焦、骁龙 8 至尊版、256GB",
    },
    {
        "id": "phone-oppo-find-x8-pro",
        "query": "OPPO Find X8 Pro",
        "name": "OPPO Find X8 Pro 12GB+256GB",
        "brand": "OPPO",
        "category": "phone",
        "price": 5299,
        "compareAt": 5699,
        "description": "双潜望长焦和哈苏影像适合旅行拍摄，机身厚度与续航控制均衡。",
        "specs": "天玑 9400、双潜望长焦、哈苏影像、5910mAh",
    },
    {
        "id": "phone-vivo-x200-pro",
        "query": "vivo X200 Pro",
        "name": "vivo X200 Pro 12GB+256GB",
        "brand": "vivo",
        "category": "phone",
        "price": 5299,
        "compareAt": 5699,
        "description": "蔡司长焦与大容量电池兼顾，适合远景、人像和高频出行场景。",
        "specs": "天玑 9400、蔡司 2 亿长焦、6000mAh、无线充电",
    },
    {
        "id": "phone-honor-magic7-pro",
        "query": "荣耀 Magic7 Pro",
        "name": "荣耀 Magic7 Pro 12GB+256GB",
        "brand": "荣耀",
        "category": "phone",
        "price": 5699,
        "compareAt": 5999,
        "description": "2 亿像素长焦与 AI 抓拍功能突出，商务设计和护眼屏适合长时间使用。",
        "specs": "骁龙 8 至尊版、2 亿长焦、AI 抓拍、5850mAh",
    },
    {
        "id": "phone-redmi-k80-pro",
        "query": "Redmi K80 Pro",
        "name": "Redmi K80 Pro 12GB+256GB",
        "brand": "小米",
        "category": "phone",
        "price": 3699,
        "compareAt": 3999,
        "description": "高性能直屏旗舰，价格更克制，适合游戏与日常高负载使用。",
        "specs": "骁龙 8 至尊版、2K 直屏、6000mAh、120W 快充",
    },
    {
        "id": "phone-oneplus-13",
        "query": "一加 13 12GB 256GB",
        "name": "一加 13 12GB+256GB",
        "brand": "一加",
        "category": "phone",
        "price": 4499,
        "compareAt": 4799,
        "description": "高刷新率屏幕和大容量电池兼顾，系统轻快，适合长期重度使用。",
        "specs": "骁龙 8 至尊版、2K 东方屏、6000mAh、100W 快充",
    },
    {
        "id": "phone-iqoo-13",
        "query": "iQOO 13 12GB 256GB",
        "name": "iQOO 13 12GB+256GB",
        "brand": "iQOO",
        "category": "phone",
        "price": 3999,
        "compareAt": 4299,
        "description": "以高性能、直屏和游戏优化为核心，兼顾日常影像和续航。",
        "specs": "骁龙 8 至尊版、2K 144Hz、6150mAh、120W 快充",
    },
    {
        "id": "phone-realme-gt7-pro",
        "query": "真我 GT7 Pro",
        "name": "realme GT7 Pro 12GB+256GB",
        "brand": "realme",
        "category": "phone",
        "price": 3599,
        "compareAt": 3999,
        "description": "大电池与高性能平台组合，面向预算明确的性能和续航用户。",
        "specs": "骁龙 8 至尊版、6500mAh、120W 快充、潜望长焦",
    },
    {
        "id": "phone-samsung-s25-ultra",
        "query": "三星 Galaxy S25 Ultra",
        "name": "三星 Galaxy S25 Ultra 12GB+256GB",
        "brand": "三星",
        "category": "phone",
        "price": 9699,
        "compareAt": 10199,
        "description": "S Pen、钛金属边框和高像素多摄系统适合商务与内容创作。",
        "specs": "骁龙 8 至尊版、2 亿主摄、S Pen、钛金属边框",
    },
    {
        "id": "phone-huawei-mate-x6",
        "query": "华为 Mate X6 折叠屏",
        "name": "HUAWEI Mate X6 12GB+256GB",
        "brand": "华为",
        "category": "phone",
        "price": 12999,
        "compareAt": 13999,
        "description": "轻薄横向折叠旗舰，适合需要大屏办公和多任务处理的用户。",
        "specs": "双旋水滴铰链、鸿蒙系统、旗舰影像、卫星通信",
    },
    {
        "id": "computer-apple-macbook-air-m4",
        "query": "MacBook Air M4 13英寸",
        "name": "Apple MacBook Air 13 英寸 M4 16GB+256GB",
        "brand": "苹果",
        "category": "computer",
        "price": 7999,
        "compareAt": 8999,
        "description": "安静无风扇、续航稳定，适合办公、学习和轻量创作。",
        "specs": "M4 芯片、16GB 统一内存、256GB SSD、13.6 英寸",
    },
    {
        "id": "computer-apple-macbook-pro-14-m4-pro",
        "query": "MacBook Pro 14 M4 Pro",
        "name": "Apple MacBook Pro 14 M4 Pro 24GB+512GB",
        "brand": "苹果",
        "category": "computer",
        "price": 12999,
        "compareAt": 14999,
        "description": "Liquid 视网膜 XDR 显示屏与专业接口配置，适合影像剪辑和开发工作。",
        "specs": "M4 Pro、24GB 统一内存、512GB SSD、14.2 英寸 XDR",
    },
    {
        "id": "computer-huawei-matebook-14",
        "query": "华为 MateBook 14 酷睿版",
        "name": "HUAWEI MateBook 14 酷睿版 16GB+1TB",
        "brand": "华为",
        "category": "computer",
        "price": 6099,
        "compareAt": 6499,
        "description": "轻薄金属机身与高分辨率触控屏，适合办公、差旅和多设备协同。",
        "specs": "酷睿 Ultra、16GB+1TB、2.8K 触控屏、轻薄机身",
    },
    {
        "id": "computer-lenovo-xiaoxin-pro-14",
        "query": "联想小新 Pro 14 2025",
        "name": "联想小新 Pro 14 2025 酷睿版",
        "brand": "联想",
        "category": "computer",
        "price": 5299,
        "compareAt": 5799,
        "description": "性能释放和屏幕素质均衡，是学生与办公用户常见的高性价比选择。",
        "specs": "酷睿 Ultra 5、16GB+1TB、2.8K 120Hz、轻薄本",
    },
    {
        "id": "computer-thinkpad-x1-carbon-13",
        "query": "ThinkPad X1 Carbon Gen 13",
        "name": "ThinkPad X1 Carbon Gen 13",
        "brand": "联想",
        "category": "computer",
        "price": 11999,
        "compareAt": 12999,
        "description": "面向商务差旅的轻薄旗舰，键盘、接口和可靠性优先。",
        "specs": "酷睿 Ultra 7、14 英寸、轻薄碳纤维机身、商务安全功能",
    },
    {
        "id": "computer-redmi-book-pro-16",
        "query": "Redmi Book Pro 16 2025",
        "name": "Redmi Book Pro 16 2025",
        "brand": "小米",
        "category": "computer",
        "price": 5999,
        "compareAt": 6499,
        "description": "大屏、高性能和整机互联兼顾，适合学生与高效办公。",
        "specs": "酷睿 Ultra、16 英寸 3.1K 屏、32GB+1TB、金属机身",
    },
    {
        "id": "computer-honor-magicbook-x16-pro",
        "query": "荣耀 MagicBook X16 Pro",
        "name": "荣耀 MagicBook X16 Pro 2025",
        "brand": "荣耀",
        "category": "computer",
        "price": 3999,
        "compareAt": 4399,
        "description": "大屏轻薄本，价格友好，适合日常办公和学习。",
        "specs": "16 英寸高色域屏、16GB+1TB、轻薄金属机身",
    },
    {
        "id": "computer-rog-zephyrus-g14",
        "query": "ROG 幻14 2025",
        "name": "ROG 幻 14 2025",
        "brand": "华硕",
        "category": "computer",
        "price": 12999,
        "compareAt": 13999,
        "description": "小尺寸高性能创作本，兼顾移动性、独显性能和 OLED 显示效果。",
        "specs": "锐龙 9、RTX 独显、14 英寸 OLED、轻薄游戏本",
    },
    {
        "id": "computer-hp-omen-10",
        "query": "惠普 暗影精灵10",
        "name": "惠普暗影精灵 10 游戏本",
        "brand": "惠普",
        "category": "computer",
        "price": 7999,
        "compareAt": 8499,
        "description": "主流高刷新率游戏本，适合高帧率网游和日常内容处理。",
        "specs": "酷睿 i7、RTX 4060、16GB+1TB、2.5K 高刷屏",
    },
    {
        "id": "computer-asus-tianxuan-6",
        "query": "华硕 天选6 Pro",
        "name": "华硕天选 6 Pro",
        "brand": "华硕",
        "category": "computer",
        "price": 7999,
        "compareAt": 8499,
        "description": "辨识度较高的主流游戏本，覆盖性能和散热需求。",
        "specs": "酷睿 Ultra、RTX 5060、16GB+1TB、2.5K 电竞屏",
    },
    {
        "id": "camera-sony-a7c-ii",
        "query": "索尼 A7C II 单机身",
        "name": "索尼 A7C II 全画幅微单",
        "brand": "索尼",
        "category": "camera",
        "price": 13999,
        "compareAt": 14999,
        "description": "轻巧全画幅机身，兼顾照片、视频与日常携带。",
        "specs": "3300 万像素、全画幅、AI 对焦、7 级防抖",
    },
    {
        "id": "camera-nikon-z8",
        "query": "尼康 Z8 单机身",
        "name": "尼康 Z8 全画幅微单",
        "brand": "尼康",
        "category": "camera",
        "price": 27999,
        "compareAt": 29999,
        "description": "高规格照片与视频性能，适合专业摄影和商业创作。",
        "specs": "4571 万像素、8K 视频、五轴防抖、专业级机身",
    },
    {
        "id": "camera-canon-r5-ii",
        "query": "佳能 EOS R5 Mark II 单机身",
        "name": "佳能 EOS R5 Mark II 全画幅微单",
        "brand": "佳能",
        "category": "camera",
        "price": 26999,
        "compareAt": 28999,
        "description": "高像素、高速连拍和专业视频规格兼顾的全画幅旗舰。",
        "specs": "4500 万像素、8K RAW、眼控对焦、机身防抖",
    },
    {
        "id": "camera-canon-r6-ii",
        "query": "佳能 EOS R6 Mark II 单机身",
        "name": "佳能 EOS R6 Mark II 全画幅微单",
        "brand": "佳能",
        "category": "camera",
        "price": 17999,
        "compareAt": 18999,
        "description": "照片与视频均衡，低光对焦和连拍能力适合进阶用户。",
        "specs": "2420 万像素、40 张每秒连拍、6K 超采样、机身防抖",
    },
    {
        "id": "camera-sony-zv-e10",
        "query": "索尼 ZV-E10 微单",
        "name": "索尼 ZV-E10 APS-C 微单",
        "brand": "索尼",
        "category": "camera",
        "price": 4899,
        "compareAt": 5299,
        "description": "面向视频创作者的可换镜头相机，收音和翻转屏设计实用。",
        "specs": "APS-C、4K 视频、实时眼部对焦、侧翻屏",
    },
    {
        "id": "camera-fujifilm-x-t5",
        "query": "富士 X-T5 微单",
        "name": "富士 X-T5 微单相机",
        "brand": "富士",
        "category": "camera",
        "price": 11990,
        "compareAt": 12990,
        "description": "复古操控、胶片模拟与高像素传感器兼具，适合静态摄影。",
        "specs": "4020 万像素、APS-C、19 种胶片模拟、机身防抖",
    },
    {
        "id": "camera-dji-osmo-pocket-3",
        "query": "大疆 Osmo Pocket 3 全能套装",
        "name": "DJI Osmo Pocket 3 全能套装",
        "brand": "大疆",
        "category": "camera",
        "price": 3499,
        "compareAt": 3799,
        "description": "一体化云台相机，适合旅行、Vlog 和移动视频创作。",
        "specs": "一英寸传感器、4K 120fps、三轴云台、旋转屏",
    },
    {
        "id": "camera-gopro-hero-13",
        "query": "GoPro Hero13 Black",
        "name": "GoPro HERO13 Black",
        "brand": "GoPro",
        "category": "camera",
        "price": 2998,
        "compareAt": 3298,
        "description": "面向运动和户外场景，防抖、防水和广角表现稳定。",
        "specs": "5.3K 视频、强防抖、10 米防水、磁吸配件",
    },
    {
        "id": "appliance-midea-air-conditioner",
        "query": "美的 1.5匹 新一级能效 空调",
        "name": "美的 1.5 匹新一级能效空调",
        "brand": "美的",
        "category": "appliance",
        "price": 2699,
        "compareAt": 2999,
        "description": "面向卧室的主流一级能效机型，兼顾节能、静音和快速制冷。",
        "specs": "1.5 匹、一级能效、变频、自清洁",
    },
    {
        "id": "appliance-gree-air-conditioner",
        "query": "格力 云锦三代 1.5匹 空调",
        "name": "格力云锦三代 1.5 匹空调",
        "brand": "格力",
        "category": "appliance",
        "price": 3299,
        "compareAt": 3599,
        "description": "格力主流中高端挂机，适合重视制冷稳定性和耐用性的家庭。",
        "specs": "1.5 匹、一级能效、变频、除菌自清洁",
    },
    {
        "id": "appliance-haier-washer-10kg",
        "query": "海尔 10公斤 滚筒洗衣机 EG100MATE29S",
        "name": "海尔 10 公斤滚筒洗衣机",
        "brand": "海尔",
        "category": "appliance",
        "price": 1709,
        "compareAt": 1999,
        "description": "10 公斤容量适合三口以上家庭，主打超薄机身和高洗净比。",
        "specs": "10kg、滚筒、一级能效、除菌螨",
    },
    {
        "id": "appliance-littleswan-washer-12kg",
        "query": "小天鹅 12公斤 滚筒洗衣机",
        "name": "小天鹅 12 公斤滚筒洗衣机",
        "brand": "小天鹅",
        "category": "appliance",
        "price": 1899,
        "compareAt": 2199,
        "description": "大容量滚筒适合家庭集中洗涤，支持蒸汽除菌和智能投放。",
        "specs": "12kg、滚筒、变频、蒸汽除菌",
    },
    {
        "id": "appliance-roborock-p10s-pro",
        "query": "石头 P10S Pro 扫地机器人",
        "name": "石头 P10S Pro 扫拖机器人",
        "brand": "石头",
        "category": "appliance",
        "price": 2599,
        "compareAt": 2999,
        "description": "自动集尘、热水洗拖布和智能避障兼顾，适合日常家庭清洁。",
        "specs": "自动集尘、热水洗拖布、热风烘干、激光导航",
    },
    {
        "id": "appliance-ecovacs-t30-pro",
        "query": "科沃斯 T30 Pro 扫地机器人",
        "name": "科沃斯 T30 Pro 扫拖机器人",
        "brand": "科沃斯",
        "category": "appliance",
        "price": 2999,
        "compareAt": 3299,
        "description": "恒压活水洗地和全能基站组合，减少日常维护频率。",
        "specs": "恒压活水洗地、热风烘干、自动集尘、智能避障",
    },
    {
        "id": "appliance-dreame-h14-pro",
        "query": "追觅 H14 Pro 洗地机",
        "name": "追觅 H14 Pro 无线洗地机",
        "brand": "追觅",
        "category": "appliance",
        "price": 2699,
        "compareAt": 2999,
        "description": "适合硬地面湿清洁，支持自清洁和热风烘干。",
        "specs": "无线洗地、热水自清洁、热风烘干、智能感应",
    },
    {
        "id": "appliance-xiaomi-tv-65",
        "query": "小米电视 S Pro 65 Mini LED",
        "name": "小米电视 S Pro 65 英寸 Mini LED",
        "brand": "小米",
        "category": "appliance",
        "price": 3499,
        "compareAt": 3999,
        "description": "高分区 Mini LED 和高刷新率组合，适合客厅影音与游戏。",
        "specs": "65 英寸、Mini LED、4K 144Hz、大内存",
    },
    {
        "id": "appliance-dyson-v12",
        "query": "戴森 V12 Detect Slim 无线吸尘器",
        "name": "戴森 V12 Detect Slim 无线吸尘器",
        "brand": "戴森",
        "category": "appliance",
        "price": 3699,
        "compareAt": 3999,
        "description": "轻量无线吸尘器，激光探测与压电传感器方便看清微尘。",
        "specs": "激光探测、150AW 吸力、轻量机身、多吸头",
    },
    {
        "id": "appliance-panasonic-hair-dryer",
        "query": "松下 纳米水离子 吹风机",
        "name": "松下纳诺怡高速吹风机",
        "brand": "松下",
        "category": "appliance",
        "price": 1099,
        "compareAt": 1299,
        "description": "高速气流和纳诺怡护发功能兼顾，适合高频日常使用。",
        "specs": "高速马达、纳诺怡、多档温风、低噪设计",
    },
]


def fetch_text(url: str) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Linux; Android 13; Pixel 7) "
                "AppleWebKit/537.36 Chrome/120 Mobile Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def clean_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def fetch_image(query: str, destination: Path) -> tuple[str | None, str]:
    encoded = urllib.parse.quote(query, safe="")
    search_url = f"https://m.suning.com/search/{encoded}/"
    try:
        page = fetch_text(search_url)
        blocks = re.findall(
            r'<li[^>]*class="def product".*?</li>',
            page,
            flags=re.DOTALL,
        )
        if not blocks:
            return None, search_url
        block = blocks[0]
        image_match = re.search(r'<img[^>]+src="([^"]+)"', block)
        title_match = re.search(
            r'<div class="pro-title"[^>]*>(.*?)</div>',
            block,
            flags=re.DOTALL,
        )
        if not image_match:
            return None, search_url
        image_url = image_match.group(1)
        if image_url.startswith("//"):
            image_url = f"https:{image_url}"
        image_url = re.sub(r"_\d+w_\d+h_4e", "_800w_800h_4e", image_url)
        result_title = clean_text(title_match.group(1)) if title_match else query
        request = urllib.request.Request(
            image_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/120 Safari/537.36"
                ),
                "Referer": search_url,
            },
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            destination.write_bytes(response.read())
        print(f"Image: {query} -> {result_title}")
        return result_title, search_url
    except Exception as error:
        print(f"Image failed: {query} ({error})")
        return None, search_url


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    catalog = []

    for index, product in enumerate(PRODUCTS, start=1):
        destination = IMAGE_DIR / f"{product['id']}.jpg"
        result_title, search_url = fetch_image(product["query"], destination)
        if not destination.exists():
            category_fallback = {
                "phone": "zol-phone-001.jpg",
                "computer": "zol-laptop-001.jpg",
                "camera": "zol-camera-001.jpg",
                "appliance": "zol-appliance-001.jpg",
            }[product["category"]]
            source_fallback = IMAGE_DIR / category_fallback
            destination.write_bytes(source_fallback.read_bytes())

        record = {
            "id": product["id"],
            "name": product["name"],
            "series": f"{CATEGORY_LABELS[product['category']]} / {index:03d}",
            "category": product["category"],
            "categoryLabel": CATEGORY_LABELS[product["category"]],
            "brand": product["brand"],
            "price": product["price"],
            "priceLabel": f"¥{product['price']}",
            "compareAt": product["compareAt"],
            "stock": 6 + ((index * 11) % 37),
            "sales": 28600 - index * 417,
            "rating": round(4.6 + ((index % 4) * 0.1), 1),
            "reviewCount": 860 + index * 93,
            "featured": index <= 4,
            "description": product["description"],
            "materials": product["specs"],
            "delivery": "现货商品预计 1 至 3 日送达，大件家电按地区预约安装。",
            "image": f"./assets/catalog/{product['id']}.jpg",
            "colors": COLOR_SETS[product["category"]],
            "source": {
                "name": "苏宁易购公开搜索结果",
                "url": search_url,
                "matchedTitle": result_title or product["query"],
                "priceText": f"参考价 ¥{product['price']}",
                "priceBasis": "品牌官方及中国主流零售平台公开页面综合参考价",
                "updatedAt": UPDATED_AT,
                "note": "价格会随地区、版本和促销活动变化，下单前以支付入口展示为准。",
            },
        }
        catalog.append(record)
        time.sleep(0.25)

    (DATA_DIR / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (DATA_DIR / "catalog.js").write_text(
        "window.MORROW_PRODUCTS = "
        + json.dumps(catalog, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(catalog)} curated products")


if __name__ == "__main__":
    main()
