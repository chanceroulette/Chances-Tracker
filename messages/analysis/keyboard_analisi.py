# messages/analysis/keyboard.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_numeric_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=6)
    buttons = [KeyboardButton(str(i)) for i in range(37)]
    for i in range(0, 36, 6):
        keyboard.row(*buttons[i:i+6])
    keyboard.row(KeyboardButton("📊 Analizza ora"))
    keyboard.row(KeyboardButton("☰ Menu"))
    return keyboard
