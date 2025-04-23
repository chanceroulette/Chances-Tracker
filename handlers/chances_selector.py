from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.state import selected_chances, user_boxes
from logic.game import initialize_boxes
from messages.keyboard import get_main_keyboard

CHANCES = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]

def show_chances_selection(bot, chat_id, suggested=None):
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = []
    for chance in CHANCES:
        text = f"✅ {chance}" if chance in selected_chances.get(chat_id, []) else chance
        buttons.append(InlineKeyboardButton(text, callback_data=f"chance_{chance}"))
    markup.add(*buttons)
    markup.add(InlineKeyboardButton("🎯 Conferma e inizia il gioco", callback_data="confirm_chances"))

    suggerite = ", ".join(suggested) if suggested else "nessuna"
    text = (
        f"🔍 *Suggerite:* {suggerite}*

"
        "Scegli le chances che vuoi usare:"
    )

    bot.send_message(
        chat_id,
        text,
        parse_mode='Markdown',
        reply_markup=markup
    )

def handle_chance_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("chance_") or call.data == "confirm_chances")
    def callback(call):
        chat_id = call.message.chat.id
        data = call.data

        if data.startswith("chance_"):
            chance = data.replace("chance_", "")
            if chat_id not in selected_chances:
                selected_chances[chat_id] = []
            if chance in selected_chances[chat_id]:
                selected_chances[chat_id].remove(chance)
            else:
                selected_chances[chat_id].append(chance)
            show_chances_selection(bot, chat_id)  # aggiorna tastiera

        elif data == "confirm_chances":
            if chat_id not in selected_chances or not selected_chances[chat_id]:
                bot.answer_callback_query(call.id, "❗Devi selezionare almeno una chance.")
                return

            # Inizializza i box per il gioco
            user_boxes[chat_id] = initialize_boxes(selected_chances[chat_id])

            bot.send_message(
                chat_id,
                f"🎯 *Gioco avviato!*
Chances attive: {', '.join(selected_chances[chat_id])}",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
