from telebot import types

# Tastiera principale con distinzione fasi
def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # 🔍 Fase Analisi
    keyboard.row("📊 Analizza", "⚡ Avvio rapido")
    
    # 🎯 Fase Gioco
    keyboard.row("🎲 Gioca", "↩️ Annulla")
    keyboard.row("📊 Statistiche", "🔄 Reset")
    
    # Generale
    keyboard.row("☰ Menu")
    
    return keyboard

# Tastiera numerica 0–36 + menu
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
    keyboard.row("☰ Menu")  # ✅ Sempre visibile
    return keyboard

# Tastiera solo per accesso all’analisi
def get_analysis_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("📊 Analizza", "⚡ Avvio rapido")
    keyboard.row("☰ Menu")
    return keyboard
