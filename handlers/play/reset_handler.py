# handlers/play/reset_handler.py
from telebot.types import Message
from logic.state import user_data
from messages.keyboard import get_main_keyboard


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "♻️ Reset")
    def reset_session(message: Message):
        chat_id = message.chat.id
        user_data[chat_id] = {
            "numbers": [],
            "selected_chances": [],
            "user_boxes": {}
        }
        bot.send_message(
            chat_id,
            "🔄 Sessione resettata. Puoi iniziare da capo.",
            reply_markup=get_main_keyboard()
        )
