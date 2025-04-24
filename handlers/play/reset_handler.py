from telebot.types import Message
from logic.state import (
    user_numbers,
    suggested_chances,
    selected_chances,
    user_boxes,
    backup_data,
    user_id_phase,
    PHASE_ANALYSIS
)
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "♻️ Reset")
    def reset(message: Message):
        user_id = message.from_user.id

        # Reset di tutte le strutture dati associate all'utente
        user_numbers.pop(user_id, None)
        suggested_chances.pop(user_id, None)
        selected_chances.pop(user_id, None)
        user_boxes.pop(user_id, None)
        backup_data.pop(user_id, None)
        user_id_phase[user_id] = PHASE_ANALYSIS

        bot.send_message(
            message.chat.id,
            "♻️ *Sessione resettata!*\nPuoi ripartire con una nuova analisi o con l'avvio rapido.",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
