# telegram_bot/views/keyboards.py

from telegram import ReplyKeyboardMarkup
from telegram_bot.views.buttons import buttons

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [buttons["train_tasks"]],
            [buttons["info"]]
        ],
        resize_keyboard=True,
        one_time_keyboard = True
    )

def get_task_buttons():
    return ReplyKeyboardMarkup(
        [
            ["4"],
            [buttons["menu"]]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_menu_keyboard():
    return ReplyKeyboardMarkup(
        [
            [buttons["menu"]]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
