from telebot.types import Message
from messages.welcome import get_welcome_message
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(commands=['start'])
    def start(message: Message):
        bot.send_message(
            message.chat.id,
            get_welcome_message(),
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
