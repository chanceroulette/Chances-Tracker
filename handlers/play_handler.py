
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from messages.keyboard import get_main_keyboard
from logic.analysis import analyze_chances
from logic.state import user_data, selected_chances, is_ready
from handlers.chances_selector import show_chances_selection

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "🎲 Gioca")
    def start_play(message: Message):
        user_id = message.from_user.id
        user_data[user_id] = []
        is_ready[user_id] = False
        bot.send_message(
            message.chat.id,
            "🎯 Inserisci *da 10 a 20 numeri* della roulette per l’analisi iniziale.",
            parse_mode='Markdown',
            reply_markup=get_number_keyboard()
        )

    @bot.message_handler(func=lambda message: message.text.isdigit() and 0 <= int(message.text) <= 36)
    def collect_number(message: Message):
        user_id = message.from_user.id
        number = int(message.text)

        if user_id not in user_data:
            user_data[user_id] = []
            is_ready[user_id] = False

        if is_ready.get(user_id, False):
            bot.send_message(message.chat.id, "⚠️ Hai già completato l’analisi. Usa il menu per continuare.")
            return

        user_data[user_id].append(number)
        count = len(user_data[user_id])

        if count < 10:
            bot.send_message(
                message.chat.id,
                f"✅ Numero *{count}* salvato: `{number}`
Ne servono almeno 10 per l’analisi.",
                parse_mode='Markdown'
            )
        elif count <= 20:
            bot.send_message(
                message.chat.id,
                f"✅ Numero *{count}* salvato: `{number}`
Premi *Analizza* per completare oppure continua (max 20 numeri).",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_message(message.chat.id, "🚫 Hai raggiunto il massimo di 20 numeri.", reply_markup=get_main_keyboard())

    @bot.message_handler(func=lambda message: message.text == "📊 Analizza")
    def analyze(message: Message):
        user_id = message.from_user.id
        numbers = user_data.get(user_id, [])

        if len(numbers) < 10:
            bot.send_message(message.chat.id, "⚠️ Servono almeno 10 numeri per analizzare.")
            return

        suggested = analyze_chances(numbers)
        show_chances_selection(bot, message.chat.id, suggested)
        is_ready[user_id] = True

# Tastiera numerica
def get_number_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for i in range(37):
        row.append(KeyboardButton(str(i)))
        if len(row) == 6:
            keyboard.row(*row)
            row = []
    if row:
        keyboard.row(*row)
    return keyboard
