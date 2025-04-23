from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.state import selected_chances
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
    bot.send_message(
        chat_id,
        f"🔍 *Suggerite:* {suggerite}\n\n"
        f"Scegli le chances che vuoi usare:",
        parse_mode='Markdown',
        reply_markup=markup
    )

def handle_chance_callbacks(call, bot):
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
        bot.send_message(
            chat_id,
            f"🎯 *Gioco avviato!*\nChances attive: {', '.join(selected_chances[chat_id])}",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
        # Qui partirà poi la logica a box (fase di gioco vera e propria)
