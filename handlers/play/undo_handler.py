# handlers/play/undo_handler.py
from telebot.types import Message
from logic.state import user_data, backup_data
from messages.keyboard import get_main_keyboard


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "↩️ Annulla")
    def undo_last(message: Message):
        chat_id = message.chat.id

        if chat_id in backup_data:
            user_data[chat_id] = backup_data[chat_id].copy()
            bot.send_message(
                chat_id,
                "↩️ Ultima giocata annullata.",
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_message(
                chat_id,
                "⚠️ Nessuna giocata precedente da annullare.",
                reply_markup=get_main_keyboard()
            )
