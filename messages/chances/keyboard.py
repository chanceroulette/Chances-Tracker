from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_chances_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)
    chances = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]
    buttons = [InlineKeyboardButton(text=chance, callback_data=f"chance:{chance}") for chance in chances]
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text="✅ Conferma", callback_data="conferma_chances"))
    return keyboard
