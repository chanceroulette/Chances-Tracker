from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from logic.analysis import analyze_chances
from logic.state import user_data, selected_chances, game_phase
from handlers.chances_selector import show_chances_selection
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "🎲 Gioca")
    def avvio_rapido(message: Message):
        user_id = message.from_user.id
        user_data[user_id] = []
        game_phase[user_id] = "scelta_rapida"
        show_chances_selection(bot, message.chat.id, suggested=None)

    @bot.message_handler(func=lambda message: message.text.isdigit() and 0 <= int(message.text) <= 36)
    def ricevi_numeri(message: Message):
        user_id = message.from_user.id
        number = int(message.text)
        if user_id not in user_data:
            user_data[user_id] = []
            game_phase[user_id] = "analisi"

        if game_phase.get(user_id) != "analisi":
            return  # ignora numeri fuori fase

        if len(user_data[user_id]) >= 20:
            bot.send_message(message.chat.id, "🚫 Hai raggiunto il massimo di 20 numeri.", reply_markup=get_main_keyboard())
            return

        user_data[user_id].append(number)
        count = len(user_data[user_id])

        if count < 10:
            bot.send_message(
                message.chat.id,
                f"✅ Numero *{count}* registrato: `{number}`. Inseriscine almeno 10.",
                parse_mode='Markdown'
            )
        elif 10 <= count < 20:
            bot.send_message(
                message.chat.id,
                f"✅ Numero *{count}* registrato: `{number}`. Premi *Analizza* oppure continua (max 20 numeri).",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_message(
                message.chat.id,
                "✅ Hai inserito 20 numeri. Ora premi *Analizza*.",
                reply_markup=get_main_keyboard()
            )

    @bot.message_handler(func=lambda message: message.text == "📊 Analizza")
    def analizza(message: Message):
        user_id = message.from_user.id
        numeri = user_data.get(user_id, [])
        if len(numeri) < 10:
            bot.send_message(message.chat.id, "⚠️ Devi inserire almeno 10 numeri per analizzare.")
            return
        game_phase[user_id] = "analisi_completa"
        suggerite = analyze_chances(numeri)
        show_chances_selection(bot, message.chat.id, suggested=suggerite)
