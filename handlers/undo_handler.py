from telebot.types import Message
from logic.state import user_data  # ✅ Import da modulo centrale

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "↩️ Annulla")
    def undo_last(message: Message):
        chat_id = message.chat.id
        if chat_id in user_data and user_data[chat_id]["numbers"]:
            last = user_data[chat_id]["numbers"].pop()
            bot.send_message(chat_id, f"🔄 Ultimo numero annullato: {last}")
        else:
            bot.send_message(chat_id, "⚠️ Nessuna giocata da annullare.")
