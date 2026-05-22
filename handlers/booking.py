import os
from datetime import datetime, timedelta
from linebot.v3.messaging import (
    FlexMessage, FlexContainer, TextMessage,
    QuickReply, QuickReplyItem, PostbackAction,
    ApiClient, Configuration, MessagingApi, PushMessageRequest
)
from supabase import create_client

_supabase = None

WAITING_NAME    = "waiting_name"
WAITING_PHONE   = "waiting_phone"
WAITING_ADDRESS = "waiting_address"


def get_supabase():
    global _supabase
    if _supabase is None:
        _supabase = create_client(
            os.environ.get("SUPABASE_URL"),
            os.environ.get("SUPABASE_KEY")
        )
    return _supabase


# ── 對話狀態管理 ────────────────────────────────

def get_session(user_id):
    try:
        r = get_supabase().table("user_sessions").select("*").eq("user_id", user_id).maybe_single().execute()
        return r.data
    except Exception as e:
        print(f"[session get error] {e}")
        return None


def _upsert_session(data):
    try:
        get_supabase().table("user_sessions").upsert(data).execute()
    except Exception as e:
        print(f"[session upsert error] {e}")


def _delete_session(user_id):
    try:
        get_supabase().table("user_sessions").delete().eq("user_id", user_id).execute()
    except Exception as e:
        print(f"[session delete error] {e}")


# ── 預約流程 ─────────────────────────────────────

def start_booking(product=None, appt_type="丈量預約"):
    quick_items = []
    for i in range(1, 8):
        date = datetime.now() + timedelta(days=i)
        label = date.strftime("%m/%d (%a)")
        data = f"action=select_date&date={date.strftime('%Y-%m-%d')}&appt_type={appt_type}"
        if product:
            data += f"&product={product}"
        quick_items.append(
            QuickReplyItem(action=PostbackAction(label=label, data=data))
        )
    icon = "📅" if appt_type == "丈量預約" else "🏠"
    return TextMessage(
        text=f"{icon} {appt_type}\n\n請選擇希望的日期：",
        quick_reply=QuickReply(items=quick_items)
    )


def select_time(date, product=None, appt_type="丈量預約"):
    times = ["10:00", "14:00", "16:00"]
    quick_items = []
    for t in times:
        data = f"action=select_time&date={date}&time={t}&appt_type={appt_type}"
        if product:
            data += f"&product={product}"
        quick_items.append(
            QuickReplyItem(action=PostbackAction(label=t, data=data))
        )
    return TextMessage(
        text=f"📅 已選擇 {date}\n\n請選擇希望的時段：",
        quick_reply=QuickReply(items=quick_items)
    )


def ask_for_name(user_id, appt_type, date, time, product=None):
    """選完時段後，建立 session 開始收集資料"""
    _upsert_session({
        "user_id": user_id,
        "state": WAITING_NAME,
        "appt_type": appt_type,
        "date": date,
        "time": time,
        "product": product,
    })
    return TextMessage(text="好的！請問您的姓名？")


def handle_name_input(user_id, name, session):
    _upsert_session({"user_id": user_id, "state": WAITING_PHONE, "name": name,
                     "appt_type": session["appt_type"], "date": session["date"],
                     "time": session["time"], "product": session.get("product")})
    return TextMessage(text=f"謝謝 {name}！\n\n📱 請問您的聯絡電話？")


def handle_phone_input(user_id, phone, session):
    _upsert_session({"user_id": user_id, "state": WAITING_ADDRESS, "phone": phone,
                     "name": session.get("name"), "appt_type": session["appt_type"],
                     "date": session["date"], "time": session["time"],
                     "product": session.get("product")})
    label = "到府丈量" if session["appt_type"] == "丈量預約" else "門市所在"
    return TextMessage(text=f"📍 請問您的地址？")


def handle_address_input(user_id, address, session):
    appt_type = session["appt_type"]
    date      = session["date"]
    time      = session["time"]
    product   = session.get("product")
    name      = session.get("name", "")
    phone     = session.get("phone", "")

    record = {
        "user_id": user_id,
        "appt_type": appt_type,
        "date": date,
        "time": time,
        "product": product,
        "name": name,
        "phone": phone,
        "address": address,
        "status": "pending",
    }
    try:
        get_supabase().table("bookings").insert(record).execute()
    except Exception as e:
        print(f"[Supabase error] {e}")

    _delete_session(user_id)
    push_owner_notification(appt_type, date, time, name, phone, address, product)
    return _confirmation_card(appt_type, date, time, name, product)


# ── 推播通知 ─────────────────────────────────────

def push_owner_notification(appt_type, date, time, name, phone, address, product):
    owner_id = os.environ.get("OWNER_LINE_USER_ID")
    token    = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    if not owner_id or not token:
        return
    try:
        product_text = f"\n📦 商品：{product}" if product else ""
        msg = (
            f"📬 新預約申請\n\n"
            f"🏷 類型：{appt_type}\n"
            f"👤 姓名：{name}\n"
            f"📱 電話：{phone}\n"
            f"📍 地址：{address}\n"
            f"📅 日期：{date}\n"
            f"🕐 時間：{time}{product_text}"
        )
        config = Configuration(access_token=token)
        with ApiClient(config) as client:
            MessagingApi(client).push_message(
                PushMessageRequest(to=owner_id, messages=[TextMessage(text=msg)])
            )
    except Exception as e:
        print(f"[push notify error] {e}")


# ── 確認卡片 ─────────────────────────────────────

def _confirmation_card(appt_type, date, time, name, product):
    icon = "📅" if appt_type == "丈量預約" else "🏠"
    rows = [
        {"label": "類型", "value": f"{icon} {appt_type}"},
        {"label": "姓名", "value": name},
        {"label": "日期", "value": date},
        {"label": "時間", "value": time},
    ]
    if product:
        rows.append({"label": "商品", "value": product})

    contents = []
    for row in rows:
        contents.append({
            "type": "box", "layout": "horizontal",
            "contents": [
                {"type": "text", "text": row["label"], "size": "sm", "color": "#888888", "flex": 2},
                {"type": "text", "text": row["value"], "size": "sm", "flex": 5, "wrap": True},
            ]
        })

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box", "layout": "vertical",
            "contents": [
                {"type": "text", "text": "✅ 預約申請已收到",
                 "weight": "bold", "size": "xl", "color": "#5C8D5E"},
                {"type": "separator", "margin": "md"},
                {"type": "box", "layout": "vertical", "margin": "md",
                 "spacing": "sm", "contents": contents},
                {"type": "separator", "margin": "md"},
                {"type": "text",
                 "text": "我們將請專人與您確認時間，謝謝！",
                 "size": "xs", "color": "#888888", "wrap": True, "margin": "md"},
            ],
        },
    }
    return FlexMessage(
        alt_text=f"預約申請已收到 {date} {time}",
        contents=FlexContainer.from_dict(bubble)
    )
