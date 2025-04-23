from telebot import types

def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # 🧠 Fase di analisi
    keyboard.row("📊 Analizza", "⚡ Avvio rapido")

    # 🎯 Fase di gioco
    keyboard.row("🎲 Gioca", "↩️ Annulla")
    keyboard.row("📊 Statistiche", "🔄 Reset")

    # Opzioni generali
    keyboard.row("☰ Menu")

    return keyboard
