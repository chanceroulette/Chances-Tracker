# callbacks.py
from telebot.types import CallbackQuery
from logic.state import selected_chances, user_numbers
from logic.game import initialize_boxes
from messages.keyboard import get_game_keyboard

# Toggle chance attiva/disattiva
def toggle_chance(call: CallbackQuery, bot):
    chat_id = call.message.chat.id
    chance = call.data.replace("toggle_", "")
    selected = selected_chances.get(chat_id, [])

    if chance in selected:
        selected.remove(chance)
    else:
        selected.append(chance)

    selected_chances[chat_id] = selected

    text = (
        f"✅ Chances attive: *{', '.join(selected) if selected else 'nessuna'}*\n"
        "Scegli o modifica le chances da usare:"
    )
    bot.edit_message_text(
        text,
        chat_id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=call.message.reply_markup
    )

# Conferma le chances e passa alla fase di gioco

def conferma_chances(call: CallbackQuery, bot):
    chat_id = call.message.chat.id
    chances = selected_chances.get(chat_id, [])
    if not chances:
        bot.answer_callback_query(call.id, "⚠️ Seleziona almeno una chance.", show_alert=True)
        return

    initialize_boxes(chat_id, chances)

    bot.edit_message_text(
        f"✅ Chances confermate: *{', '.join(chances)}*\n"
        f"🎯 Inserisci i numeri della roulette uno alla volta usando la tastiera numerica.",
        chat_id,
        call.message.message_id,
        parse_mode="Markdown",
        reply_markup=get_game_keyboard()
    )
