from telebot.types import Message
from messages.keyboard_generale import get_main_keyboard

def handle_start(bot, message: Message):
    bot.send_message(
        message.chat.id,
        "👋 Benvenuto nel bot *Chance Tracker™*!\n\n"
        "🎯 Inserisci i numeri usciti alla roulette (da 0 a 36).\n"
        "📊 Dopo almeno 10 numeri potrai premere *Analizza* per ricevere le chances suggerite.",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
