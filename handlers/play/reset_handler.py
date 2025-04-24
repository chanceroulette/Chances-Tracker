from telebot.types import Message
from logic.state import (
    user_numbers,
    selected_chances,
    suggested_chances,
    user_boxes,
    user_id_phase
)
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "♻️ Reset")
    def reset(message: Message):
        user_id = message.from_user.id

        user_numbers.pop(user_id, None)
        selected_chances.pop(user_id, None)
        suggested_chances.pop(user_id, None)
        user_boxes.pop(user_id, None)
        user_id_phase.pop(user_id, None)

        bot.send_message(
            message.chat.id,
            "🔄 Sessione *completamente resettata*.",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
