from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from logic.analysis import analyze_chances
from logic.state import user_data, selected_chances, game_phase
from messages.keyboard import get_main_keyboard
from handlers.chances_selector import show_chances_selection


def register(bot):
    @bot.message_handler(func=lambda message: message.text == "📊 Analizza")
    def start_analysis(message: Message):
        user_id = message.from_user.id
        game_phase[user_id] = "analisi"
        user_data[user_id] = []

        # Tastiera numerica 0–36
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        row = []
        for i in range(37):
            row.append(KeyboardButton(str(i)))
            if len(row) == 6:
                keyboard.row(*row)
                row = []
        if row:
            keyboard.row(*row)

        bot.send_message(
            message.chat.id,
            "🎯 *Inserisci da 10 a 20 numeri* della roulette usando la tastiera numerica.",
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    @bot.message_handler(func=lambda message: message.text.isdigit() and 0 <= int(message.text) <= 36)
    def collect_numbers(message: Message):
        user_id = message.from_user.id
        number = int(message.text)

        if game_phase.get(user_id) != "analisi":
            return

        user_data.setdefault(user_id, []).append(number)
        count = len(user_data[user_id])

        if count < 10:
            bot.send_message(
                message.chat.id,
                f"✅ Numero *{count}* registrato: `{number}`. Continua fino a 10 o più numeri...",
                parse_mode='Markdown'
            )
        elif count < 20:
            bot.send_message(
                message.chat.id,
                f"✅ Numero *{count}* registrato: `{number}`. Premi *Analizza* oppure continua (max 20 numeri).",
                parse_mode='Markdown'
            )
        else:
            bot.send_message(
                message.chat.id,
                f"✅ Hai inserito il numero massimo consentito. Procedo all’analisi...",
                parse_mode='Markdown'
            )
            chances = analyze_chances(user_data[user_id])
            show_chances_selection(bot, message.chat.id, user_id, chances)
            game_phase[user_id] = "selezione"

    @bot.message_handler(func=lambda message: message.text == "📊 Analizza ora")
    def analyze_now(message: Message):
        user_id = message.from_user.id
        if user_id not in user_data or len(user_data[user_id]) < 10:
            bot.send_message(
                message.chat.id,
                "⚠️ Inserisci almeno *10 numeri* prima di analizzare.",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
            return

        chances = analyze_chances(user_data[user_id])
        show_chances_selection(bot, message.chat.id, user_id, chances)
        game_phase[user_id] = "selezione"
