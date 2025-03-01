# telegram_bot/utils/subscription.py

from telegram_bot.config import settings


async def check_subscription(user_id, context):
    CHANNEL_ID = settings["CHANNEL_ID"]
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False
