from telebot import types

# Tastiera principale con distinzione fasi
def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # 🔍 Fase di Analisi
    keyboard.row("📊 Analizza", "⚡ Avvio rapido")
    
    # 🎯 Fase di Gioco
    keyboard.row("🎲 Gioca", "↩️ Annulla")
    keyboard.row("📊 Statistiche", "🔄 Reset")
    
    # Generale
    keyboard.row("☰ Menu")
    
    return keyboard

# Tastiera numerica 0–36
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

# Tastiera analisi fase 1
def get_analysis_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.row("📊 Analizza", "⚡ Avvio rapido")
    keyboard.row("☰ Menu")
    return keyboard
