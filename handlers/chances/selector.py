from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

CHANCES = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]

# Mostra tastiera inline con chances

def get_chance_markup(suggerite=None):
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = []
    for chance in CHANCES:
        emoji = "✅" if suggerite and chance in suggerite else "➖"
        buttons.append(InlineKeyboardButton(f"{emoji} {chance}", callback_data=f"toggle_{chance}"))
    markup.add(*buttons)
    markup.add(InlineKeyboardButton("✅ Conferma", callback_data="confirm_chances"))
    return markup

# Funzione per mostrare la selezione delle chances
def show_chances_selection(bot, message, suggerite=None):
    markup = get_chance_markup(suggerite)
    msg = f"🔍 *Suggerite:* {', '.join(suggerite)}\n_Seleziona manualmente le chances che vuoi attivare._"
    bot.send_message(message.chat.id, msg, parse_mode="Markdown", reply_markup=markup)
