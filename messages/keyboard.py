from telebot import types

# Tastiera principale
def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.row("☰ Menu", "🎲 Gioca")
    keyboard.row("↩️ Annulla", "📊 Statistiche")
    keyboard.row("🔄 Reset")
    return keyboard

# Tastiera numerica per inserimento numeri
def get_number_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for i in range(37):
        row.append(types.KeyboardButton(str(i)))
        if len(row) == 6:
            keyboard.row(*row)
            row = []
    if row:
        keyboard.row(*row)
    keyboard.row("↩️ Annulla", "🔄 Reset")
    return keyboard

# Tastiera per fase di analisi (con avvio rapido)
def get_analysis_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.row("📊 Analizza", "⚡ Avvio rapido")
    keyboard.row("☰ Menu")
    return keyboard
