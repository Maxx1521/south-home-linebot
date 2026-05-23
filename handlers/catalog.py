from linebot.v3.messaging import (
    FlexMessage, FlexContainer, TextMessage,
)

CATEGORY_META = {
    "海島型實木地板": {
        "image": "https://images.unsplash.com/photo-1567225557594-88d73e55f2cb?w=800",
        "price_from": "NT$ 9,350",
    },
    "超耐磨木地板": {
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800",
        "price_from": "NT$ 3,700",
    },
    "石塑地板": {
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
        "price_from": "NT$ 3,250",
    },
    "塑膠地磚": {
        "image": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800",
        "price_from": "NT$ 2,300",
    },
    "戶外塑木地板": {
        "image": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800",
        "price_from": "洽詢門市",
    },
}

CATEGORY_ORDER = ["海島型實木地板", "超耐磨木地板", "石塑地板", "塑膠地磚", "戶外塑木地板"]

# 超耐磨木地板：品牌 → 款式
LAMINATE_BRANDS = {
    "山井富士山": {
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800",
        "products": [
            {"name": "典藏款", "desc": "（描述待補）", "price": "NT$ 3,700/坪"},
            {"name": "尊爵款", "desc": "（描述待補）", "price": "NT$ 4,250/坪"},
        ],
    },
    "派斯吐司倒角": {
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800",
        "products": [
            {"name": "派斯吐司倒角系列", "desc": "（描述待補）", "price": "NT$ 4,500/坪"},
        ],
    },
    "森WoodLand": {
        "image": "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800",
        "products": [
            {"name": "一般款", "desc": "（描述待補）", "price": "NT$ 5,200/坪"},
            {"name": "人字拼", "desc": "（描述待補）", "price": "NT$ 7,100/坪"},
        ],
    },
    "Krono畢卡索": {
        "image": "https://images.unsplash.com/photo-1580237541049-2d715a09486e?w=800",
        "products": [
            {"name": "寬長款", "desc": "（描述待補）", "price": "NT$ 6,800/坪"},
            {"name": "人字拼", "desc": "（描述待補）", "price": "NT$ 7,500/坪"},
        ],
    },
    "德國EGGER": {
        "image": "https://images.unsplash.com/photo-1560185893-a55cbc8c57e8?w=800",
        "products": [
            {"name": "黃標", "desc": "（描述待補）", "price": "NT$ 4,300/坪"},
            {"name": "紅標", "desc": "（描述待補）", "price": "NT$ 5,100/坪"},
            {"name": "綠標", "desc": "（描述待補）", "price": "NT$ 5,500/坪"},
            {"name": "藍標", "desc": "（描述待補）", "price": "NT$ 5,900/坪"},
            {"name": "人字拼", "desc": "（描述待補）", "price": "NT$ 7,300/坪"},
        ],
    },
    "羅賓地板": {
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800",
        "products": [
            {"name": "羅賓地板", "desc": "（描述待補）", "price": "NT$ 3,700/坪"},
        ],
    },
    "都華地板": {
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800",
        "products": [
            {"name": "都華地板", "desc": "（描述待補）", "price": "NT$ 3,700/坪"},
        ],
    },
}

# 其他分類：直接列商品
PRODUCTS = {
    "海島型實木地板": [
        {
            "name": "Ua雙橡園",
            "desc": "（描述待補）",
            "price": "NT$ 9,350~12,300/坪",
            "image": "https://images.unsplash.com/photo-1567225557594-88d73e55f2cb?w=800",
        },
    ],
    "石塑地板": [
        {"name": "愛麗絲 法國系列", "desc": "（描述待補）", "price": "NT$ 3,250/坪", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"},
        {"name": "愛麗絲 英倫系列", "desc": "（描述待補）", "price": "NT$ 3,700/坪", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"},
        {"name": "派斯 石紋", "desc": "（描述待補）", "price": "NT$ 4,500/坪", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"},
        {"name": "派斯 木紋", "desc": "（描述待補）", "price": "NT$ 4,500/坪", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"},
        {"name": "酷石 石紋S系列", "desc": "（描述待補）", "price": "NT$ 3,900/坪", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"},
        {"name": "酷石 水磨石W系列", "desc": "（描述待補）", "price": "NT$ 4,200/坪", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"},
        {"name": "酷石 歐洲EU系列", "desc": "（描述待補）", "price": "NT$ 3,900/坪", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"},
        {"name": "酷石 歐洲EU人字拼", "desc": "（描述待補）", "price": "NT$ 5,700/坪", "image": "https://images.unsplash.com/photo-1580237541049-2d715a09486e?w=800"},
        {"name": "酷石 微水泥系列", "desc": "（描述待補）", "price": "NT$ 6,000/坪", "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800"},
        {"name": "寶陞 人字拼", "desc": "（描述待補）", "price": "NT$ 6,500/坪", "image": "https://images.unsplash.com/photo-1580237541049-2d715a09486e?w=800"},
    ],
    "塑膠地磚": [
        {"name": "石系列", "desc": "（描述待補）", "price": "NT$ 2,300/坪", "image": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800"},
        {"name": "樹系列", "desc": "（描述待補）", "price": "NT$ 2,300/坪", "image": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800"},
    ],
    "戶外塑木地板": [],
}


def _product_bubble(p, product_key):
    return {
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
                        "data": f"action=booking&product={product_key}",
                    },
                }
            ],
        },
    }


def get_category_flex():
    bubbles = []
    for category in CATEGORY_ORDER:
        meta = CATEGORY_META[category]
        if category == "超耐磨木地板":
            count_text = f"{len(LAMINATE_BRANDS)} 個品牌"
        elif not PRODUCTS.get(category):
            count_text = "敬請期待"
        else:
            count_text = f"{len(PRODUCTS[category])} 款商品"

        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": meta["image"],
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": category, "weight": "bold", "size": "lg"},
                    {"type": "text", "text": count_text, "size": "sm", "color": "#888888", "margin": "sm"},
                    {"type": "text", "text": f"從 {meta['price_from']}", "size": "sm", "color": "#4CAF50", "margin": "sm"},
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
    if category == "超耐磨木地板":
        return _laminate_brands_flex()

    products = PRODUCTS.get(category, [])
    if not products:
        return TextMessage(text="此分類商品即將上架，歡迎來電或到門市詢問！")

    bubbles = [_product_bubble(p, p["name"]) for p in products]
    carousel = {"type": "carousel", "contents": bubbles}
    return FlexMessage(alt_text=f"{category} 商品列表", contents=FlexContainer.from_dict(carousel))


def _laminate_brands_flex():
    bubbles = []
    for brand, info in LAMINATE_BRANDS.items():
        prices = [p["price"] for p in info["products"]]
        price_text = prices[0] if len(prices) == 1 else f"{prices[0].split('/')[0]} 起"
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": info["image"],
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": brand, "weight": "bold", "size": "md"},
                    {"type": "text", "text": f"{len(info['products'])} 款", "size": "sm", "color": "#888888", "margin": "sm"},
                    {"type": "text", "text": price_text, "size": "sm", "color": "#4CAF50", "margin": "sm"},
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
                            "label": "查看款式",
                            "data": f"action=view_brand&brand={brand}",
                        },
                    }
                ],
            },
        }
        bubbles.append(bubble)

    carousel = {"type": "carousel", "contents": bubbles}
    return FlexMessage(alt_text="超耐磨木地板品牌", contents=FlexContainer.from_dict(carousel))


def get_brand_products_flex(brand):
    info = LAMINATE_BRANDS.get(brand)
    if not info:
        return TextMessage(text="找不到此品牌，請重新選擇。")

    bubbles = []
    for p in info["products"]:
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": info["image"],
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": brand, "size": "sm", "color": "#888888"},
                    {"type": "text", "text": p["name"], "weight": "bold", "size": "md", "margin": "sm"},
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
                            "data": f"action=booking&product={brand} {p['name']}",
                        },
                    }
                ],
            },
        }
        bubbles.append(bubble)

    carousel = {"type": "carousel", "contents": bubbles}
    return FlexMessage(alt_text=f"{brand} 款式", contents=FlexContainer.from_dict(carousel))
