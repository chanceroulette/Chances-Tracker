from telebot.types import ReplyKeyboardMarkup, KeyboardButton

CHANCES = ["🔴 Rosso", "⚫ Nero", "🟢 Pari", "🟡 Dispari", "🔵 Manque", "🟣 Passe"]
CONFIRM = "✅ Conferma selezione"
CANCEL = "❌ Annulla selezione"

# Stato per ciascun utente: scelte attive
selected_chances = {}

def show_chances_selector(bot, chat_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, len(CHANCES), 2):
        keyboard.row(KeyboardButton(CHANCES[i]), KeyboardButton(CHANCES[i+1]))
    keyboard.row(KeyboardButton(CONFIRM), KeyboardButton(CANCEL))
    keyboard.row(KeyboardButton("☰ Menu"))

    selected_chances[chat_id] = set()  # Reset scelte
    bot.send_message(
        chat_id,
        "🎯 *Seleziona le chances* su cui vuoi giocare.\n"
        "✅ Premi *Conferma selezione* quando sei pronto.",
        parse_mode='Markdown',
        reply_markup=keyboard
    )

def register(bot):
    from logic.state import active_chances, user_phase

    @bot.message_handler(func=lambda msg: msg.text in CHANCES)
    def select_chance(msg):
        chat_id = msg.chat.id
        choice = msg.text

        if chat_id not in selected_chances:
            selected_chances[chat_id] = set()

        if choice in selected_chances[chat_id]:
            selected_chances[chat_id].remove(choice)
            bot.send_message(chat_id, f"❎ {choice} rimosso.")
        else:
            selected_chances[chat_id].add(choice)
            bot.send_message(chat_id, f"✅ {choice} selezionato.")

    @bot.message_handler(func=lambda msg: msg.text == CONFIRM)
    def confirm_chances(msg):
        chat_id = msg.chat.id
        chosen = list(selected_chances.get(chat_id, []))

        if not chosen:
            bot.send_message(chat_id, "⚠️ Seleziona almeno una chance prima di confermare.")
            return

        active_chances[chat_id] = chosen
        user_phase[chat_id] = "play"

        bot.send_message(
            chat_id,
            f"🎮 *Inizio gioco!* Chances attive: {', '.join(chosen)}",
            parse_mode='Markdown'
        )
        # TODO: Avvia sistema a box (fase 2)
