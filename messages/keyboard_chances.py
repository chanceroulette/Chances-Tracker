from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_chances_keyboard(suggested=None):
    all_chances = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = []

    for chance in all_chances:
        prefix = "✅ " if suggested and chance in suggested else ""
        buttons.append(InlineKeyboardButton(text=f"{prefix}{chance}", callback_data=f"chance_{chance}"))

    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton("✔️ Conferma", callback_data="confirm_chances"))
    return keyboard
