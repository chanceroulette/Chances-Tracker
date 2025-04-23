# handlers/play/play_handler.py

from telebot.types import Message
from logic.state import user_data, selected_chances
from messages.keyboard import get_main_keyboard, get_numeric_keyboard
from logic.game import initialize_boxes
from messages.play import get_start_message

def register(bot):
    @bot.message_handler(func=lambda m: m.text == "🎲 Gioca")
    def entry_point(message: Message):
        chat_id = message.chat.id

        if chat_id not in selected_chances or not selected_chances[chat_id]:
            bot.send_message(
                chat_id,
                "⚠️ Devi prima selezionare le *chances* da usare! Usa /analizza o Avvio rapido.",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
            return

        # Inizializza stato utente per il gioco
        user_data[chat_id] = {
            "phase": "insert_game_numbers",
            "numbers": [],
            "history": [],
            "chances": selected_chances[chat_id],
            "boxes": initialize_boxes(selected_chances[chat_id])
        }

        bot.send_message(
            chat_id,
            get_start_message(selected_chances[chat_id]),
            parse_mode='Markdown',
            reply_markup=get_numeric_keyboard()
        )
