# telegram_bot/controllers/task_controller.py

from telegram import Update
from telegram.ext import CallbackContext
from telegram_bot.views import keyboards
from .task_4_controller import start_task_4, handle_task_callback

async def select_task(update: Update, context: CallbackContext):
    reply_markup = keyboards.get_task_buttons()
    await update.message.reply_text("Выберите номер задания (от 1 до 26):", reply_markup=reply_markup)

async def start_training(update: Update, context: CallbackContext, task_number: int):
    if task_number == 4:
        await start_task_4(update, context)
    else:
        reply_markup = keyboards.get_main_keyboard()
        await update.message.reply_text(
            f"Задание №{task_number} еще не готово. Следи за новостями.",
            reply_markup=reply_markup
        )