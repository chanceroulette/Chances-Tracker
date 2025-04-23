from telebot.types import Message
from messages.keyboard import get_main_keyboard, get_number_keyboard
from messages.chances_selector import show_chances_selector
from logic.analysis import analyze_chances
from logic.state import user_data
from logic.state import active_chances  # nuovo dizionario

def register(bot):
    # Inserimento numeri per analisi
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

    # Raccolta numeri
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
                "Ora puoi avviare la fase di gioco con 🎲 Gioca.",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )

    # Avvio rapido
    @bot.message_handler(func=lambda message: message.text == "⚡ Avvio rapido")
    def avvio_rapido(message: Message):
        user_id = message.from_user.id
        user_data[user_id] = []  # Reset eventuale sessione
        active_chances[user_id] = []  # Reset scelte rapide
        show_chances_selector(bot, message.chat.id)

    # Gestione selezione chance
    @bot.message_handler(func=lambda message: message.text in ["🔴 Rosso", "⚫️ Nero", "🔵 Pari", "🟠 Dispari", "🟢 Manque (1–18)", "🔴 Passe (19–36)"])
    def select_chance(message: Message):
        user_id = message.from_user.id
        choice = message.text
        if user_id not in active_chances:
            active_chances[user_id] = []

        if choice not in active_chances[user_id]:
            active_chances[user_id].append(choice)
            bot.send_message(message.chat.id, f"✅ Aggiunta: *{choice}*", parse_mode="Markdown")

    # Conferma chances
    @bot.message_handler(func=lambda message: message.text == "✅ Conferma selezione")
    def conferma_chances(message: Message):
        user_id = message.from_user.id
        chances = active_chances.get(user_id, [])

        if not chances:
            bot.send_message(
                message.chat.id,
                "⚠️ Nessuna chance selezionata.",
                reply_markup=get_main_keyboard()
            )
        else:
            bot.send_message(
                message.chat.id,
                f"✅ Hai selezionato: {', '.join(chances)}\n\nPuoi iniziare a giocare con 🎲 Gioca.",
                reply_markup=get_main_keyboard(),
                parse_mode="Markdown"
            )

    # Annulla selezione
    @bot.message_handler(func=lambda message: message.text == "❌ Annulla")
    def annulla_rapido(message: Message):
        user_id = message.from_user.id
        active_chances.pop(user_id, None)
        bot.send_message(
            message.chat.id,
            "❌ Selezione annullata.",
            reply_markup=get_main_keyboard()
        )
