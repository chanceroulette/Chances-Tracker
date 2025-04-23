from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from messages.keyboard import get_main_keyboard
from logic.analysis import analyze_chances
from logic.state import user_data, selected_chances
from messages.chances_selector import show_chances_selection

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "🎯 Analizza")
    def analyze(message):
        user_id = message.from_user.id
        user_data[user_id] = []
        bot.send_message(
            message.chat.id,
            "🎯 Inserisci i primi *15 numeri* della roulette usando la tastiera numerica.",
            parse_mode='Markdown',
            reply_markup=get_number_keyboard()
        )

    @bot.message_handler(func=lambda message: message.text == "⚡ Avvio rapido")
    def quick_start(message):
        user_id = message.from_user.id
        selected_chances[user_id] = []
        show_chances_selection(bot, message.chat.id, suggestions=[])

    @bot.message_handler(func=lambda message: message.text.isdigit() and 0 <= int(message.text) <= 36)
    def collect_number(message):
        user_id = message.from_user.id
        number = int(message.text)
        if user_id not in user_data:
            user_data[user_id] = []
        user_data[user_id].append(number)
        count = len(user_data[user_id])

        if count < 15:
            bot.send_message(
                message.chat.id,
                f"✅ Numero *{count}* salvato: `{number}`\n{15 - count} ancora...",
                parse_mode='Markdown'
            )
        else:
            numbers = user_data[user_id]
            chances = analyze_chances(numbers)
            del user_data[user_id]
            bot.send_message(
                message.chat.id,
                f"✅ *Numeri completati!*\n\n📊 *Chances consigliate:* {', '.join(chances)}",
                parse_mode='Markdown'
            )
            show_chances_selection(bot, message.chat.id, suggestions=chances)

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
    keyboard.row(KeyboardButton("☰ Menu"))
    return keyboard
