from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "🎲 Gioca")
    def play(message):
        # Stato utente su "inserimento numeri"
        bot.send_message(
            message.chat.id,
            "🎯 Inserisci i primi *15 numeri* della roulette usando la tastiera numerica.\n\n"
            "_Serviranno per analizzare le chances migliori._",
            parse_mode='Markdown',
            reply_markup=get_number_keyboard()
        )

# Tastiera numerica inline (0–36)
def get_number_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for i in range(37):
        row.append(KeyboardButton(str(i)))
        if len(row) == 6:
            keyboard.row(*row)
            row = []
    if row:
        keyboard.row(*row)
    return keyboard
