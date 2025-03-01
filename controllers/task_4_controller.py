# telegram_bot/controllers/task_4_controller.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from telegram_bot.models.task_4_model import generate_question
from telegram_bot.views.task_4_views import (
    get_task4_menu,
    render_question,
    render_result,
    send_theory_document
)


async def handle_task_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "start_training_4":
        context.user_data.clear()
        generate_question(context)
        await show_question(update, context)
    
    elif data.startswith("select_"):
        number = data.split("_")[1]
        selected = context.user_data.setdefault('selected', set())
        if number in selected:
            selected.remove(number)
        else:
            selected.add(number)
        await show_question(update, context)
    
    elif data == "submit":
        await handle_answer(update, context)
    
    elif data == "next_question":
        generate_question(context)
        context.user_data.pop('selected', None)
        await show_question(update, context)
    
    elif data == "theory_4":
        message = await send_theory_document(update, context)
        await query.edit_message_text(message)


async def show_question(update: Update, context: CallbackContext):
    try:
        question = context.user_data['current_question']
        selected = context.user_data.get('selected', set())
        text, markup = render_question(question, selected)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=markup)
        else:
            await update.message.reply_text(text, reply_markup=markup)
    except KeyError:
        error_msg = "Произошла ошибка, попробуйте еще раз."
        if update.callback_query:
            await update.callback_query.edit_message_text(error_msg)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=error_msg)


async def handle_answer(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    
    question = context.user_data['current_question']
    selected = context.user_data.get('selected', set())
    user_choices = {int(num) - 1 for num in selected}
    
    is_correct = user_choices == set(question['correct_indices'])
    response = render_result(question, selected, is_correct)
    
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Следующий вопрос", callback_data="next_question")]
    ])
    
    await query.edit_message_text(response, reply_markup=markup)


async def start_task_4(update: Update, context: CallbackContext):
    await update.message.reply_text("Выберите действие:", reply_markup=get_task4_menu())