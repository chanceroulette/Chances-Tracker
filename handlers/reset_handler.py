from handlers.play_handler import user_data
from handlers.undo_handler import backup_data
from messages.keyboard import get_main_keyboard
from telebot.types import Message

def register(bot):
    @bot.message_handler(commands=["reset"])
    @bot.message_handler(func=lambda message: message.text.lower() in ["reset", "🔄 Reset"])
    def reset(message: Message):
        user_id = message.from_user.id
        user_data.pop(user_id, None)
        backup_data.pop(user_id, None)

        bot.send_message(
            message.chat.id,
            "🔄 Sessione azzerata! Puoi iniziare una nuova sequenza con 🎲 Gioca.",
            reply_markup=get_main_keyboard()
        )
