from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from logic.analysis import analyze_chances
from logic.state import user_data
from messages.keyboard import get_main_keyboard

# Salva chances selezionate per avviare il gioco successivamente
active_chances = {}

def register(bot):
    @bot.message_handler(commands=["analizza"])
    @bot.message_handler(func=lambda message: message.text == "📊 Analizza")
    def start_analysis(message: Message):
        user_id = message.from_user.id
        user_data[user_id] = []
        bot.send_message(
            message.chat.id,
            "📊 Inserisci almeno *15 numeri* della roulette per analizzare le chances migliori.",
            parse_mode='Markdown',
            reply_markup=get_number_keyboard()
        )

    @bot.message_handler(func=lambda message: message.text.isdigit() and 0 <= int(message.text) <= 36)
    def collect_analysis_data(message: Message):
        user_id = message.from_user.id
        number = int(message.text)

        if user_id not in user_data:
            user_data[user_id] = []

        user_data[user_id].append(number)
        count = len(user_data[user_id])

        if count < 15:
            bot.send_message(
                message.chat.id,
                f"✅ Numero {count} salvato: `{number}`\n{15 - count} ancora...",
                parse_mode='Markdown'
            )
        else:
            chances = analyze_chances(user_data[user_id])
            active_chances[user_id] = chances
            user_data.pop(user_id)

            bot.send_message(
                message.chat.id,
                f"📊 *Chances consigliate:* {', '.join(chances)}\n\n"
                "Ora puoi avviare la fase di gioco con 🎮 Gioca.",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )

    @bot.message_handler(func=lambda message: message.text == "⚡ Avvio rapido")
    def avvio_rapido(message: Message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Rosso", "Nero")
        markup.row("Pari", "Dispari")
        markup.row("Manque", "Passe")
        markup.row("✅ Conferma selezione", "❌ Annulla")
        bot.send_message(
            message.chat.id,
            "⚡ *Avvio rapido*: seleziona manualmente le chances che vuoi attivare.",
            parse_mode='Markdown',
            reply_markup=markup
        )
