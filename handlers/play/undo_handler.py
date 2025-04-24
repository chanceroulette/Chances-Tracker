from telebot.types import Message
from logic.state import user_numbers, backup_data
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "↩️ Annulla")
    def undo(message: Message):
        user_id = message.from_user.id

        if user_id in backup_data:
            user_numbers[user_id] = backup_data[user_id]
            del backup_data[user_id]

            bot.send_message(
                message.chat.id,
                "↩️ Ultima giocata *annullata*.",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_message(
                message.chat.id,
                "⚠️ Nessuna giocata da annullare.",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
