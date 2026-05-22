"""
一次性執行：建立 LINE 圖文選單（Rich Menu）
執行方式：python setup_richmenu.py
"""
import os, requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

W, H = 2500, 843
COL = W // 3  # 每格寬度 833

# ── 建立選單結構 ──────────────────────────────
menu = {
    "size": {"width": W, "height": H},
    "selected": True,
    "name": "南島家居主選單",
    "chatBarText": "開啟服務選單",
    "areas": [
        {
            "bounds": {"x": 0, "y": 0, "width": COL, "height": H},
            "action": {"type": "postback", "data": "action=booking&appt_type=丈量預約", "label": "丈量預約"}
        },
        {
            "bounds": {"x": COL, "y": 0, "width": COL, "height": H},
            "action": {"type": "postback", "data": "action=store_visit", "label": "門市參觀"}
        },
        {
            "bounds": {"x": COL * 2, "y": 0, "width": COL + 1, "height": H},
            "action": {"type": "postback", "data": "action=color_selection", "label": "線上選色"}
        },
    ]
}

r = requests.post(
    "https://api.line.me/v2/bot/richmenu",
    headers={**HEADERS, "Content-Type": "application/json"},
    json=menu
)
r.raise_for_status()
menu_id = r.json()["richMenuId"]
print(f"✅ 建立選單：{menu_id}")

# ── 產生圖片 ──────────────────────────────────
img = Image.new("RGB", (W, H), "#F5F0E8")
draw = ImageDraw.Draw(img)

panels = [
    {"color": "#3D6B4F", "emoji": "📅", "title": "丈量預約", "sub": "到府丈量服務"},
    {"color": "#5A8A5E", "emoji": "🏠", "title": "門市參觀", "sub": "預約門市參觀"},
    {"color": "#7AAD7E", "emoji": "🎨", "title": "線上選色", "sub": "瀏覽色系目錄"},
]

# 嘗試載入中文字型
try:
    font_title = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 100)
    font_sub   = ImageFont.truetype("C:/Windows/Fonts/msjh.ttc", 55)
    font_emoji = ImageFont.truetype("C:/Windows/Fonts/seguiemj.ttf", 130)
except Exception as e:
    print(f"字型載入失敗，使用預設：{e}")
    font_title = ImageFont.load_default()
    font_sub   = font_title
    font_emoji = font_title

for i, p in enumerate(panels):
    x0 = i * COL
    x1 = x0 + COL
    cx = x0 + COL // 2

    # 背景
    draw.rectangle([x0, 0, x1, H], fill=p["color"])

    # 分隔線
    if i > 0:
        draw.line([x0, 30, x0, H - 30], fill="rgba(255,255,255,80)", width=2)

    # Emoji
    draw.text((cx, 280), p["emoji"], fill="white", font=font_emoji, anchor="mm")
    # 主標題
    draw.text((cx, 520), p["title"], fill="white", font=font_title, anchor="mm")
    # 副標題
    draw.text((cx, 640), p["sub"], fill="#D4ECD8", font=font_sub, anchor="mm")

img.save("richmenu.png", quality=95)
print("✅ 圖片產生：richmenu.png")

# ── 上傳圖片 ──────────────────────────────────
with open("richmenu.png", "rb") as f:
    r = requests.post(
        f"https://api-data.line.me/v2/bot/richmenu/{menu_id}/content",
        headers={**HEADERS, "Content-Type": "image/png"},
        data=f
    )
r.raise_for_status()
print(f"✅ 圖片上傳完成")

# ── 設為預設選單 ──────────────────────────────
r = requests.post(
    f"https://api.line.me/v2/bot/user/all/richmenu/{menu_id}",
    headers=HEADERS
)
r.raise_for_status()
print(f"✅ 已設為預設選單")
print(f"\n🎉 完成！選單 ID：{menu_id}")
