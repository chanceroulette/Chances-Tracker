# messages/keyboard_generale.py

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        KeyboardButton("☰ Menu"),
        KeyboardButton("↩️ Annulla"),
        KeyboardButton("🔄 Reset")
    )
    keyboard.row(
        KeyboardButton("🎲 Avvio rapido"),
        KeyboardButton("🧮 Analizza"),
        KeyboardButton("📊 Statistiche")
    )
    return keyboard

def get_numeric_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, 37, 6):
        row = [KeyboardButton(str(j)) for j in range(i, min(i + 6, 37))]
        keyboard.row(*row)
    keyboard.row(KeyboardButton("📊 Analizza"))
    keyboard.row(KeyboardButton("☰ Menu"))
    return keyboard
