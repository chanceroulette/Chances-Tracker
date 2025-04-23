# analysis/insert_handler.py

from telebot.types import Message
from messages.keyboard import get_numeric_keyboard, get_main_keyboard
from logic.state import user_data
from logic.utils import count_inserted

def register(bot):
    @bot.message_handler(func=lambda msg: msg.text == "🧮 Analizza")
    def start_insert(msg: Message):
        user_id = msg.from_user.id
        user_data[user_id] = []
        bot.send_message(
            msg.chat.id,
            "🎯 Inizia l’inserimento dei numeri usciti (minimo 10, massimo 20):",
            reply_markup=get_numeric_keyboard()
        )

    @bot.message_handler(func=lambda msg: msg.text.isdigit() and 0 <= int(msg.text) <= 36)
    def collect_numbers(msg: Message):
        user_id = msg.from_user.id
        number = int(msg.text)
        numbers = user_data.setdefault(user_id, [])

        if len(numbers) >= 20:
            bot.send_message(msg.chat.id, "⚠️ Hai già inserito 20 numeri.", reply_markup=get_main_keyboard())
            return

        numbers.append(number)
        remaining = max(10 - len(numbers), 0)
        status = f"✅ Inserito: `{number}` — Totale: {len(numbers)}"

        if len(numbers) < 10:
            status += f"\n🔄 Ne servono ancora: {remaining}"
        else:
            status += "\n👉 Puoi premere '📊 Analizza' o continuare a inserire fino a 20 numeri."

        bot.send_message(msg.chat.id, status, parse_mode="Markdown", reply_markup=get_numeric_keyboard())
