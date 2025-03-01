# telegram_bot/controllers/bot_controller.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot.views.buttons import buttons
from telegram_bot.utils.subscription import check_subscription
from telegram_bot.views import keyboards, messages
from telegram_bot.controllers import task_controller

async def start(update, context):
    user_id = update.message.from_user.id
    if await check_subscription(user_id, context):
        reply_markup = keyboards.get_main_keyboard()
        await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)
    else:
        await send_start_menu(update, context)

async def handle_message(update, context):
    user_id = update.message.from_user.id
    if not await check_subscription(user_id, context):
        await send_start_menu(update, context)
        return
    text = update.message.text
    if text == buttons["train_tasks"]:
        await task_controller.select_task(update, context)
    elif text == buttons["info"]:
        await update.message.reply_text(messages.get_info_message())
    elif text == buttons["menu"]:
        reply_markup = keyboards.get_main_keyboard()
        await update.message.reply_text("Меню:", reply_markup=reply_markup)
    elif text.isdigit() and 1 <= int(text) <= 26:
        task_number = int(text)
        await task_controller.start_training(update, context, task_number)
    else:
        reply_markup = keyboards.get_main_keyboard()
        await update.message.reply_text(messages.get_invalid_input_message(), reply_markup=reply_markup)

async def send_start_menu(update, context):
    welcome_text = messages.get_welcome_message()
    await update.message.reply_text(welcome_text)
    keyboard = [[InlineKeyboardButton(buttons["check_subscription"], callback_data="check_subscription")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажмите кнопку ниже, чтобы проверить подписку:", reply_markup=reply_markup)

async def check_subscription_callback(update, context):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if await check_subscription(user_id, context):
        reply_markup = keyboards.get_main_keyboard()
        await query.edit_message_text("Спасибо за подписку! Теперь вы можете начать тренировку.")
        await context.bot.send_message(chat_id=user_id, text="Выберите действие:", reply_markup=reply_markup)
    else:
        await query.edit_message_text("Вы не подписаны на канал. Пожалуйста, подпишитесь и попробуйте снова.")