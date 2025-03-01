# telegram_bot/views/messages.py

from telegram_bot.config import settings
from telegram_bot.views.buttons import buttons


def get_info_message():
    return f"""⭐️ Основная информация:
            Создатель: @ivan_blkh
            Канал бота: {settings["URL"]}
            
            ⁉️ Вот что я умею:
            Наверное, вы уже знаете, чем я занимаюсь, но я всё-таки расскажу:
            
            🤖 Я — бот для тренировки заданий ЕГЭ. Нажмите кнопку {buttons["train_tasks"]}, чтобы продолжить.
            """


def get_welcome_message():
    return f"""
            Привет! Я бот-тренажер для подготовки к ЕГЭ по русскому языку.

            Для начала работы подпишитесь на наш канал: {settings["URL"]}
            """


def get_invalid_input_message(): return "Неверный ввод. Выберите доступную команду:"
