from linebot.v3.messaging import TextMessage
from handlers.booking import _upsert_session, _delete_session

WAITING_AREA = "waiting_area"

# 請填入實際門市地址（地區關鍵字 → 地址）
STORE_LOCATIONS = {
    "台北": "台北市○○區○○路○○號",
    "新北": "新北市○○區○○路○○號",
    "桃園": "桃園市○○區○○路○○號",
}

DEFAULT_STORE = "台北市○○區○○路○○號（總店）"


def start_location_inquiry(user_id):
    _upsert_session({"user_id": user_id, "state": WAITING_AREA})
    return TextMessage(text="請問您在哪個地區呢？我們將傳送最近門市的地址給您 🏠")


def handle_area_input(user_id, area):
    _delete_session(user_id)
    for key, address in STORE_LOCATIONS.items():
        if key in area:
            return TextMessage(
                text=f"🏠 離您最近的門市：\n\n"
                     f"📍 地址：{address}\n\n"
                     f"歡迎前來參觀！\n如需預約，請輸入「門市參觀」。"
            )
    return TextMessage(
        text=f"🏠 我們的門市：\n\n"
             f"📍 地址：{DEFAULT_STORE}\n\n"
             f"歡迎前來參觀！\n如需預約，請輸入「門市參觀」。"
    )
