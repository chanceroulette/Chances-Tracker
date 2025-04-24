from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.state import suggested_chances, selected_chances, user_id_phase, PHASE_SELECTION
from messages.chances_keyboard import get_chances_keyboard
from telebot import TeleBot
from telebot.types import Message

def show_chances_selection(bot: TeleBot, message: Message, chances):
    user_id = message.from_user.id
    suggested_chances[user_id] = chances
    selected_chances[user_id] = []  # reset scelta
    user_id_phase[user_id] = PHASE_SELECTION

    suggerite = ', '.join(chances)

    bot.send_message(
        message.chat.id,
        f"🔍 *Suggerite:* {suggerite}\n\n"
        "✋ Seleziona le chances con cui vuoi giocare.\n"
        "✅ Premi *Conferma* per avviare il sistema.",
        parse_mode='Markdown',
        reply_markup=get_chance_markup(chances)
    )

def get_chance_markup(chances):
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=chance, callback_data=f"toggle_{chance}") for chance in chances]
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton("✅ Conferma", callback_data="confirm_chances"))
    return keyboard

def register(bot: TeleBot):
    # Non ci sono handler da registrare al momento, ma la funzione è qui per evitare errori
    print("✅ selector.py caricato — nessun handler registrato, solo funzioni di supporto.")
