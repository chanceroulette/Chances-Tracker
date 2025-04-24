from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from logic.state import user_numbers, user_id_phase, PHASE_ANALYSIS
from logic.keyboards import get_numeric_keyboard, get_analysis_keyboard

MAX_NUMBERS = 20
MIN_NUMBERS = 10

def handle_number_input(bot, message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    # Verifica se è un numero valido tra 0 e 36
    if not text.isdigit() or not (0 <= int(text) <= 36):
        bot.send_message(message.chat.id, "❌ Inserisci un numero valido tra 0 e 36.")
        return

    number = int(text)
    numbers = user_numbers.get(user_id, [])
    numbers.append(number)
    user_numbers[user_id] = numbers

    count = len(numbers)

    if count < MIN_NUMBERS:
        bot.send_message(
            message.chat.id,
            f"✅ Numero {count} salvato: *{number}*.\nInserisci almeno {MIN_NUMBERS} numeri.",
            parse_mode='Markdown',
            reply_markup=get_numeric_keyboard()
        )

    elif MIN_NUMBERS <= count < MAX_NUMBERS:
        bot.send_message(
            message.chat.id,
            f"✅ Numero {count} salvato: *{number}*.\nHai inserito abbastanza numeri.\nPremi 📊 *Analizza* oppure continua fino a {MAX_NUMBERS}.",
            parse_mode='Markdown',
            reply_markup=get_analysis_keyboard()
        )

    elif count == MAX_NUMBERS:
        bot.send_message(
            message.chat.id,
            f"✅ Numero {count} salvato: *{number}*.\n📊 Hai inserito il massimo di numeri consentiti.",
            parse_mode='Markdown',
            reply_markup=get_analysis_keyboard()
        )
        user_id_phase[user_id] = PHASE_ANALYSIS
