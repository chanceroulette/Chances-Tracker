# analyze_handler.py
from telebot.types import Message
from logic.state import user_numbers
from handlers.chances.selector import show_chances_selection
from messages.analysis.keyboard import get_numeric_keyboard

def register(bot):
    @bot.message_handler(func=lambda msg: msg.text == "📊 Analizza ora")
    def handle_analysis(message: Message):
        chat_id = message.chat.id
        numbers = user_numbers.get(chat_id, [])

        if len(numbers) < 10:
            bot.send_message(chat_id, "⚠️ Devi inserire almeno 10 numeri per analizzare.", reply_markup=get_numeric_keyboard())
            return

        bot.send_message(chat_id, "🌯 Analisi in corso...", reply_markup=None)
        show_chances_selection(bot, chat_id, numbers)
