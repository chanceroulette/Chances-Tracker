from telebot.types import Message
from handlers.chances_selector import show_chances_selection
from logic.state import user_data
from messages.keyboard import get_number_keyboard, get_main_keyboard


def register(bot):
    # Comando "📊 Analizza"
    @bot.message_handler(func=lambda message: message.text == "📊 Analizza")
    def start_analysis(message: Message):
        user_id = message.from_user.id
        user_data[user_id] = []

        bot.send_message(
            message.chat.id,
            "🎯 Inserisci i numeri della roulette uno alla volta usando la tastiera numerica.",
            parse_mode='Markdown',
            reply_markup=get_number_keyboard()
        )

    # Inserimento dei numeri per l’analisi
    @bot.message_handler(func=lambda message: message.text.isdigit() and 0 <= int(message.text) <= 36)
    def collect_number(message: Message):
        user_id = message.from_user.id
        number = int(message.text)

        if user_id not in user_data:
            user_data[user_id] = []

        user_data[user_id].append(number)
        count = len(user_data[user_id])

        if count < 10:
            bot.send_message(
                message.chat.id,
                f"✅ Numero {count} registrato: `{number}`. Inseriscine almeno 10.",
                parse_mode='Markdown'
            )
        elif count < 20:
            bot.send_message(
                message.chat.id,
                f"✅ Numero {count} registrato: `{number}`.\nPremi *📊 Analizza ora* oppure continua (max 20 numeri).",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_message(
                message.chat.id,
                f"✅ Numero 20 registrato: `{number}`. Avvio analisi...",
                parse_mode='Markdown'
            )
            show_chances_selection(bot, message.chat.id, user_data[user_id])

    # Avvio analisi manuale
    @bot.message_handler(func=lambda message: message.text == "📊 Analizza ora")
    def analyze_now(message: Message):
        user_id = message.from_user.id
        if user_id not in user_data or len(user_data[user_id]) < 10:
            bot.send_message(
                message.chat.id,
                "⚠️ Devi inserire almeno 10 numeri per analizzare.",
                reply_markup=get_main_keyboard()
            )
            return

        show_chances_selection(bot, message.chat.id, user_data[user_id])

    # Avvio rapido senza inserimento numeri
    @bot.message_handler(func=lambda message: message.text == "⚡ Avvio rapido")
    def quick_start(message: Message):
        user_id = message.from_user.id
        user_data[user_id] = []  # reset per sicurezza
        show_chances_selection(bot, message.chat.id, [])  # analisi vuota → scelta manuale
