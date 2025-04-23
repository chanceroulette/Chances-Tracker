# handlers/analysis/insert_handler.py

from telebot.types import Message
from logic.state import user_numbers
from messages.analysis.keyboard import get_numeric_keyboard

def register(bot):
    @bot.message_handler(func=lambda msg: msg.text.isdigit() and 0 <= int(msg.text) <= 36)
    def handle_number_input(message: Message):
        chat_id = message.chat.id
        number = int(message.text)

        if chat_id not in user_numbers:
            user_numbers[chat_id] = []

        if len(user_numbers[chat_id]) >= 20:
            bot.send_message(chat_id, "⚠️ Hai già inserito 20 numeri. Premi '📊 Analizza ora' oppure resetta.")
            return

        user_numbers[chat_id].append(number)
        response = f"✅ Numero {len(user_numbers[chat_id])} registrato: *{number}*"
        if len(user_numbers[chat_id]) < 10:
            response += ". Inseriscine almeno 10."
        elif len(user_numbers[chat_id]) == 10:
            response += ". Premi *Analizza ora* oppure continua (max 20 numeri)."
        else:
            response += ". Puoi ancora inserirne fino a 20 o premere *Analizza ora*."

        bot.send_message(chat_id, response, parse_mode="Markdown", reply_markup=get_numeric_keyboard())
