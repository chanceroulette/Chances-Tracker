from telebot.types import Message
from logic.state import user_data, backup_data
from messages.keyboard import get_main_keyboard
from messages.keyboard import get_number_keyboard

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "↩️ Annulla")
    def undo(message: Message):
        user_id = message.from_user.id

        if user_id in backup_data:
            user_data[user_id] = backup_data[user_id].copy()
            bot.send_message(
                message.chat.id,
                "↩️ Ultima giocata ripristinata!\nPuoi continuare a inserire i numeri.",
                reply_markup=get_number_keyboard()
            )
        else:
            bot.send_message(
                message.chat.id,
                "⚠️ Nessuna giocata da annullare.",
                reply_markup=get_main_keyboard()
            )
