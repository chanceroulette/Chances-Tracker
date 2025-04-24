from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_numeric_keyboard():
    """
    Tastiera numerica da 0 a 36 per l’inserimento dei numeri della roulette.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=6)
    buttons = [KeyboardButton(str(i)) for i in range(37)]
    for i in range(0, 37, 6):
        keyboard.add(*buttons[i:i+6])
    return keyboard

def get_analysis_keyboard():
    """
    Tastiera con il pulsante per avviare l'analisi dopo aver inserito almeno 10 numeri.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("📊 Analizza"))
    return keyboard
