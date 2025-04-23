from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from logic.state import selected_chances
from messages.keyboard import get_main_keyboard

CHANCES = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]

def show_chances_selection(bot, chat_id, suggested=None):
    suggested = suggested or []
    selected_chances[chat_id] = set(suggested)

    text = "🔍 *Suggerite:* " + (", ".join(suggested) if suggested else "_nessuna_") + "\n\n"
    text += "Scegli le chances che vuoi usare:"

    markup = InlineKeyboardMarkup(row_width=3)
    for chance in CHANCES:
        active = "✅ " if chance in selected_chances[chat_id] else "▫️"
        markup.add(InlineKeyboardButton(f"{active} {chance}", callback_data=f"toggle_{chance}"))
    markup.add(InlineKeyboardButton("🎯 Conferma e inizia il gioco", callback_data="confirm_chances"))

    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)

def handle_chance_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_") or call.data == "confirm_chances")
    def callback(call: CallbackQuery):
        chat_id = call.message_
