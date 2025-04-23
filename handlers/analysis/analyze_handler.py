# analysis/analyze_handler.py

from telebot.types import Message
from logic.state import user_data
from handlers.chances import selector
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(func=lambda msg: msg.text == "📊 Analizza")
    def analyze_and_select(msg: Message):
        user_id = msg.from_user.id
        numbers = user_data.get(user_id, [])

        if len(numbers) < 10:
            bot.send_message(
                msg.chat.id,
                "⚠️ Devi inserire almeno 10 numeri prima di analizzare.",
                reply_markup=get_main_keyboard()
            )
            return

        bot.send_message(msg.chat.id, "🔍 Analisi in corso...")
        selector.show_chances_selection(bot, msg.chat.id, numbers)
