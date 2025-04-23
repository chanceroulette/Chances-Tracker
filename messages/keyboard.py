from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Tastiera principale con tutti i comandi principali
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("📊 Analizza"), KeyboardButton("⚡ Avvio rapido"))
    keyboard.row(KeyboardButton("🎲 Gioca"), KeyboardButton("↩️ Annulla"))
    keyboard.row(KeyboardButton("📊 Statistiche"), KeyboardButton("🔁 Reset"))
    keyboard.row(KeyboardButton("☰ Menu"))
    return keyboard

# Tastiera numerica per l'inserimento dei numeri
def get_number_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(str(i)) for i in range(37)]
    for i in range(0, len(buttons), 6):
        keyboard.row(*buttons[i:i+6])
    keyboard.row(KeyboardButton("📊 Analizza ora"), KeyboardButton("☰ Menu"))
    return keyboard

# Tastiera di gioco (durante la fase con sistema a box)
def get_game_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton("🎲 Gioca"), KeyboardButton("↩️ Annulla"))
    keyboard.row(KeyboardButton("📊 Statistiche"), KeyboardButton("🔁 Reset"))
    keyboard.row(KeyboardButton("☰ Menu"))
    return keyboard
