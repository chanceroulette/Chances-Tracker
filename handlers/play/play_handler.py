# handlers/play/play_handler.py
from telebot.types import Message
from logic.state import user_data
from messages.keyboard import get_main_keyboard


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "🎲 Gioca")
    def entry_point(message: Message):
        chat_id = message.chat.id

        # Inizializza o resetta lo stato dell’utente per il gioco
        user_data[chat_id] = {
            "phase": "insert_game_numbers",
            "numbers": [],
            "history": [],
            "chances": [],
            "boxes": {}
        }

        bot.send_message(
            chat_id,
            "🎯 Inserisci i numeri estratti dal gioco per iniziare a seguire la tua strategia.",
            reply_markup=get_main_keyboard()
        )
