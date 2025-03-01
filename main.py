# telegram_bot/main.py

from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram_bot.config import settings
from telegram_bot.controllers import bot_controller, task_controller


def main():
    app = Application.builder().token(settings["TOKEN"]).build()
    
    app.add_handler(CommandHandler('start', bot_controller.start))
    app.add_handler(CallbackQueryHandler(
        bot_controller.check_subscription_callback,
        pattern="check_subscription"
    ))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        bot_controller.handle_message
    ))
    app.add_handler(CallbackQueryHandler(
        task_controller.handle_task_callback,
        pattern=r"^(start_training_4|submit|next_question|select_|theory_4)"
    ))
    
    app.run_polling()


if __name__ == '__main__':
    main()