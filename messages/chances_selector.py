from telebot.types import ReplyKeyboardMarkup

def show_chances_selector(bot, chat_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    keyboard.row("🔴 Rosso", "⚫️ Nero")
    keyboard.row("🔵 Pari", "🟠 Dispari")
    keyboard.row("🟢 Manque (1–18)", "🔴 Passe (19–36)")
    keyboard.row("✅ Conferma selezione", "❌ Annulla")

    bot.send_message(
        chat_id,
        "🎯 *Seleziona manualmente* le chances che vuoi attivare per la sessione di gioco:\n\n"
        "Scegli liberamente tra le 6 opzioni qui sotto.\n"
        "Puoi confermare appena hai finito. 👇",
        parse_mode='Markdown',
        reply_markup=keyboard
    )
