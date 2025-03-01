# telegram_bot/views/task_4_views.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram_bot.views.buttons import buttons
import os


from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot.views.buttons import buttons

def get_task4_menu():
    keyboard = [
        [InlineKeyboardButton(buttons["start_training"], callback_data="start_training_4")],
        [InlineKeyboardButton(buttons["theory"], callback_data="theory_4")]
    ]
    return InlineKeyboardMarkup(keyboard)


def render_question(question, selected=None):
    text = "Выберите слова с правильным ударением:\n\n" + "\n".join(
        f"{i + 1}. {word}" for i, word in enumerate(question['words'])
    )

    buttons_row = []
    for i in range(5):
        emoji = "✅" if str(i + 1) in (selected or set()) else "⬜"
        buttons_row.append(
            InlineKeyboardButton(f"{i + 1} {emoji}", callback_data=f"select_{i + 1}")
        )
    
    keyboard = [
        buttons_row,
        [InlineKeyboardButton("Ответить", callback_data="submit")]
    ]
    
    return text, InlineKeyboardMarkup(keyboard)


def render_result(question, selected, is_correct):
    correct_indices = sorted(question['correct_indices'])
    
    user_choices = ', '.join(sorted(selected)) if selected else "нет ответа"
    correct_answer = ', '.join(str(i + 1) for i in correct_indices)
    
    words_list = [f"{i + 1}. {word}" for i, word in enumerate(question['words'])]
    
    return (
            f"{'✅ Правильный ответ' if is_correct else '❌ Неправильный ответ'}\n\n"
            f"Ваш выбор: {user_choices}\n"
            f"Правильные ответы: {correct_answer}\n\n"
            "Слова:\n" + '\n'.join(words_list)
    )

async def send_theory_document(update, context):
    try:
        base_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'task_4')
        file_path = os.path.join(base_path, 'theory.docx')
        with open(file_path, 'rb') as file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=InputFile(file, filename="Теория_задание_4.docx")
            )
        return "Теория отправлена!"
    except FileNotFoundError:
        return "Файл теории не найден"