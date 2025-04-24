# ✅ File: messages/chances_keyboard.py

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.state import selected_chances

CHANCES = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]

# Genera tastiera con le chances da selezionare
def get_chances_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = []

    for chance in CHANCES:
        selected = "✅ " if chance in selected_chances.get(user_id, []) else ""
        buttons.append(
            InlineKeyboardButton(f"{selected}{chance}", callback_data=f"chance_{chance}")
        )

    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton("✅ Conferma", callback_data="confirm_chances"))
    return keyboard
