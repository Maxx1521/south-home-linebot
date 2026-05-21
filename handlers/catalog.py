import json
from linebot.v3.messaging import (
    FlexMessage, FlexContainer,
    ReplyMessageRequest, TextMessage,
    QuickReply, QuickReplyItem, PostbackAction
)

# 產品分類資料（之後可改為從 Supabase 讀取）
CATEGORIES = {
    "超耐磨木地板": [
        {
            "name": "橡木紋 經典系列",
            "desc": "耐刮防水，適合全室鋪設",
            "price": "NT$ 1,200/坪起",
            "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800",
        },
        {
            "name": "胡桃木紋 深色系列",
            "desc": "沉穩質感，北歐風首選",
            "price": "NT$ 1,500/坪起",
            "image": "https://images.unsplash.com/photo-1580237541049-2d715a09486e?w=800",
        },
        {
            "name": "淺色霧面系列",
            "desc": "日式清新，好清潔維護",
            "price": "NT$ 1,350/坪起",
            "image": "https://images.unsplash.com/photo-1560185893-a55cbc8c57e8?w=800",
        },
    ],
    "SPC石塑地板": [
        {
            "name": "防水SPC 米色系",
            "desc": "100% 防水，適合廚房浴室",
            "price": "NT$ 900/坪起",
            "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
        },
        {
            "name": "防水SPC 灰色系",
            "desc": "現代工業風格，超耐用",
            "price": "NT$ 950/坪起",
            "image": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
        },
    ],
    "實木地板": [
        {
            "name": "柚木實木地板",
            "desc": "天然原木紋理，頂級質感",
            "price": "NT$ 3,500/坪起",
            "image": "https://images.unsplash.com/photo-1567225557594-88d73e55f2cb?w=800",
        },
        {
            "name": "橡木實木地板",
            "desc": "歐洲進口，耐久美觀",
            "price": "NT$ 4,200/坪起",
            "image": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800",
        },
    ],
}


def get_category_flex():
    bubbles = []
    for category, products in CATEGORIES.items():
        first = products[0]
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": first["image"],
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": category, "weight": "bold", "size": "lg"},
                    {"type": "text", "text": f"{len(products)} 款商品", "size": "sm", "color": "#888888", "margin": "sm"},
                    {"type": "text", "text": f"從 {products[0]['price']}", "size": "sm", "color": "#4CAF50", "margin": "sm"},
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#5C8D5E",
                        "action": {
                            "type": "postback",
                            "label": "查看商品",
                            "data": f"action=view_category&category={category}",
                        },
                    }
                ],
            },
        }
        bubbles.append(bubble)

    carousel = {"type": "carousel", "contents": bubbles}
    return FlexMessage(alt_text="產品目錄", contents=FlexContainer.from_dict(carousel))


def get_products_flex(category):
    products = CATEGORIES.get(category, [])
    if not products:
        return TextMessage(text="找不到此分類商品，請重新選擇。")

    bubbles = []
    for p in products:
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": p["image"],
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": p["name"], "weight": "bold", "size": "md"},
                    {"type": "text", "text": p["desc"], "size": "sm", "color": "#666666", "margin": "sm", "wrap": True},
                    {"type": "text", "text": p["price"], "size": "sm", "color": "#4CAF50", "margin": "md", "weight": "bold"},
                ],
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#5C8D5E",
                        "action": {
                            "type": "postback",
                            "label": "預約到府丈量",
                            "data": f"action=booking&product={p['name']}",
                        },
                    }
                ],
            },
        }
        bubbles.append(bubble)

    carousel = {"type": "carousel", "contents": bubbles}
    return FlexMessage(alt_text=f"{category} 商品列表", contents=FlexContainer.from_dict(carousel))
