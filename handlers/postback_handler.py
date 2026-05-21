from urllib.parse import parse_qs
from linebot.v3.messaging import ReplyMessageRequest, TextMessage
from handlers.catalog import get_category_flex, get_products_flex
from handlers.booking import start_booking, select_time, confirm_booking


def handle_postback(event, line_bot_api):
    data = parse_qs(event.postback.data)
    action = data.get("action", [""])[0]
    user_id = event.source.user_id

    if action == "catalog":
        reply = get_category_flex()

    elif action == "view_category":
        category = data.get("category", [""])[0]
        reply = get_products_flex(category)

    elif action == "booking":
        product = data.get("product", [None])[0]
        reply = start_booking(product)

    elif action == "select_date":
        date = data.get("date", [""])[0]
        product = data.get("product", [None])[0]
        reply = select_time(date, product)

    elif action == "select_time":
        date = data.get("date", [""])[0]
        time = data.get("time", [""])[0]
        product = data.get("product", [None])[0]
        reply = confirm_booking(user_id, date, time, product)

    else:
        reply = TextMessage(text="請輸入「選單」查看服務項目。")

    line_bot_api.reply_message(
        ReplyMessageRequest(reply_token=event.reply_token, messages=[reply])
    )
