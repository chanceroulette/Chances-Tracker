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
        chat_id = call.message.chat.id
        data = call.data

        if data.startswith("toggle_"):
            chance = data.split("_", 1)[1]
            if chance in selected_chances.get(chat_id, set()):
                selected_chances[chat_id].remove(chance)
            else:
                selected_chances.setdefault(chat_id, set()).add(chance)
            show_chances_selection(bot, chat_id, list(selected_chances[chat_id]))
        elif data == "confirm_chances":
            if not selected_chances.get(chat_id):
                bot.answer_callback_query(call.id, "⚠️ Seleziona almeno una chance.")
                return

            bot.edit_message_text(
                "✅ *Chances confermate!*\nInizia ora la fase di gioco.",
                chat_id,
                call.message.message_id,
                parse_mode='Markdown'
            )
            # Avvia fase gioco con box
            from handlers.play_handler import start_box_phase
            start_box_phase(bot, chat_id, list(selected_chances[chat_id]))

            # Tastiera principale
            bot.send_message(chat_id, "🎮 Sistema attivo. Buon gioco!", reply_markup=get_main_keyboard())
