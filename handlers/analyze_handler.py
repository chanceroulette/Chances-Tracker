from telebot.types import Message
from logic.state import user_data
from messages.keyboard import get_number_keyboard
from handlers.chances_selector import show_chances_selection

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "🔍 Analizza")
    def analyze(message: Message):
        user_id = message.from_user.id

        if user_id not in user_data or len(user_data[user_id]) < 10:
            bot.send_message(
                message.chat.id,
                "⚠️ Devi inserire almeno *10 numeri* prima di avviare l'analisi.",
                parse_mode="Markdown"
            )
            return

        if len(user_data[user_id]) > 20:
            user_data[user_id] = user_data[user_id][:20]

        numeri = user_data[user_id]
        show_chances_selection(bot, message.chat.id, numeri)
