# handlers/analysis/insert_handler.py

from telebot.types import Message
from messages.keyboard import get_numeric_keyboard
from logic import state

def register(bot):
    @bot.message_handler(func=lambda message: message.text.isdigit())
    def handle_number_input(message: Message):
        chat_id = message.chat.id
        number = int(message.text)

        if 0 <= number <= 36:
            user_numbers = state.user_data.setdefault(chat_id, [])
            if number not in user_numbers:
                user_numbers.append(number)
                bot.send_message(chat_id, f"Numero {number} aggiunto. Totale numeri: {len(user_numbers)}", reply_markup=get_numeric_keyboard())
            else:
                bot.send_message(chat_id, f"Il numero {number} è già stato inserito.", reply_markup=get_numeric_keyboard())
        else:
            bot.send_message(chat_id, "Inserisci un numero valido tra 0 e 36.", reply_markup=get_numeric_keyboard())
