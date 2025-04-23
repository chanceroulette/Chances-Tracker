from telebot.types import ReplyKeyboardRemove
from logic.state import user_data
from messages.keyboard import get_numeric_keyboard
from handlers.chances_selector import show_chances_selection

def register(bot):
    @bot.message_handler(commands=["analizza"])
    def start_analysis(message):
        user_id = message.from_user.id
        user_data[user_id] = {
            "numbers": [],
            "state": "collecting"
        }
        bot.send_message(
            message.chat.id,
            "🎯 Inserisci i numeri della roulette uno alla volta usando la tastiera numerica.",
            reply_markup=get_numeric_keyboard()
        )

    @bot.message_handler(func=lambda message: user_data.get(message.from_user.id, {}).get("state") == "collecting")
    def collect_numbers(message):
        user_id = message.from_user.id
        text = message.text.strip()

        if not text.isdigit() or not (0 <= int(text) <= 36):
            bot.send_message(message.chat.id, "⚠️ Inserisci un numero valido tra 0 e 36.")
            return

        num = int(text)
        user_data[user_id]["numbers"].append(num)
        count = len(user_data[user_id]["numbers"])

        if count < 10:
            bot.send_message(message.chat.id, f"✅ Numero {count} registrato: {num}. Inseriscine almeno 10.")
        elif 10 <= count < 20:
            bot.send_message(message.chat.id, f"✅ Numero {count} registrato: {num}. Premi *Analizza ora* oppure continua (max 20 numeri).", parse_mode="Markdown")
        elif count == 20:
            bot.send_message(message.chat.id, f"✅ Numero 20 registrato: {num}. Analisi automatica in corso...", parse_mode="Markdown")
            show_chances_selection(bot, message.chat.id, user_data[user_id]["numbers"])
            user_data[user_id]["state"] = "waiting"
            return

    @bot.message_handler(func=lambda message: message.text == "📊 Analizza ora")
    def analyze_now(message):
        user_id = message.from_user.id
        numbers = user_data.get(user_id, {}).get("numbers", [])

        if len(numbers) < 10:
            bot.send_message(message.chat.id, "⚠️ Devi inserire almeno 10 numeri per analizzare.")
            return

        user_data[user_id]["state"] = "waiting"
        show_chances_selection(bot, message.chat.id, numbers)
        bot.send_message(message.chat.id, "📊 Analisi completata.", reply_markup=ReplyKeyboardRemove())
