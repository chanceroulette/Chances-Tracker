from telebot import types

def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.row("☰ Menu", "🎲 Gioca")
    keyboard.row("↩️ Annulla", "📊 Statistiche")
    keyboard.row("🔄 Reset")
    return keyboard
