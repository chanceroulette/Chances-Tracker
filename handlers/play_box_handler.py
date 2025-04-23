from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from logic.analysis import analyze_chances
from logic.state import user_data, selected_chances, game_phase
from messages.keyboard import get_main_keyboard, get_number_keyboard
from handlers.chances_selector import show_chances_selection

def register(bot):

    @bot.message_handler(func=lambda message: message.text == "📊 Analizza")
    def start_analysis(message: Message):
        user_id = message.from_user.id
        game_phase[user_id] = "analisi"
        user_data[user_id] = []

        bot.send_message(
            message.chat.id,
            "🎯 *Inserisci da 10 a 20 numeri* della roulette usando la tastiera numerica.",
            parse_mode='Markdown',
            reply_markup=get_number_keyboard()
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
                f"✅ Numero *{count}* registrato: `{number}`. Inseriscine almeno 10.",
                parse_mode='Markdown',
                reply_markup=get_number_keyboard()
            )
        elif count < 20:
            bot.send_message(
                message.chat.id,
                f"✅ Numero *{count}* registrato: `{number}`. Premi *📊 Analizza ora* oppure continua (max 20 numeri).",
                parse_mode='Markdown',
                reply_markup=get_number_keyboard()
            )
        else:
            bot.send_message(
                message.chat.id,
                f"✅ Numero *{count}* registrato: `{number}`. Procedo all’analisi...",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
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
                "⚠️ Devi inserire almeno *10 numeri* per analizzare.",
                parse_mode='Markdown',
                reply_markup=get_number_keyboard()
            )
            return

        chances = analyze_chances(user_data[user_id])
        show_chances_selection(bot, message.chat.id, user_id, chances)
        game_phase[user_id] = "selezione"
