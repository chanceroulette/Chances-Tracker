from telebot.types import Message
from messages.keyboard import get_main_keyboard
from messages.welcome import get_welcome_message

def register(bot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        bot.send_message(
            message.chat.id,
            get_welcome_message(),
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )

    @bot.message_handler(commands=['menu'])
    def menu_cmd(message: Message):
        bot.send_message(
            message.chat.id,
            get_welcome_message(),
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )

    @bot.message_handler(commands=['analizza'])
    def analizza(message: Message):
        bot.send_message(
            message.chat.id,
            "📊 Inserisci *minimo 10 e massimo 20 numeri* per analizzare le chances più attive.",
            parse_mode='Markdown'
        )
        # Avvia fase raccolta numeri per analisi
        from handlers.play_handler import start_analysis
        start_analysis(bot, message)
