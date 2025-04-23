# handlers/chances/selector.py

from telebot.types import Message
from logic.state import selected_chances
from messages.chances import get_chances_keyboard
from logic.game import initialize_boxes
from messages.play import get_start_message
from messages.keyboard import get_numeric_keyboard
from messages.chances.keyboard import get_chances_keyboard
from messages.keyboard_chances import get_chances_keyboard



def show_chances_selection(bot, message: Message):
    chat_id = message.chat.id
    selected_chances[chat_id] = []

    bot.send_message(
        chat_id,
        "🎯 *Seleziona le chances con cui vuoi giocare:*\n"
        "_Puoi sceglierne una o più, poi conferma._",
        parse_mode='Markdown',
        reply_markup=get_chances_keyboard()
    )

def register(bot):
    @bot.message_handler(func=lambda m: m.text == "Avvio rapido")
    def handle_avvio_rapido(message: Message):
        show_chances_selection(bot, message)
