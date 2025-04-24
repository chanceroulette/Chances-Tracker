from telebot.types import CallbackQuery, Message
from logic.state import selected_chances, user_id_phase, PHASE_PLAY
from messages.keyboard_generale import get_main_keyboard

def handle_callback(bot, call: CallbackQuery):
    data = call.data

    if data.startswith("toggle_"):
        handle_toggle_chance(bot, call)

    elif data == "confirm_chances":
        handle_confirm_chances(bot, call)

def handle_toggle_chance(bot, call: CallbackQuery):
    user_id = call.from_user.id
    chance = call.data.replace("toggle_", "")

    selected = selected_chances.get(user_id, [])
    if chance in selected:
        selected.remove(chance)
    else:
        selected.append(chance)

    selected_chances[user_id] = selected

    # Aggiorna tastiera
    from messages.chances_keyboard import get_chances_keyboard
    markup = get_chances_keyboard(user_id)

    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )

def handle_confirm_chances(bot, call: CallbackQuery):
    user_id = call.from_user.id
    chances = selected_chances.get(user_id, [])

    if not chances:
        bot.answer_callback_query(call.id, "⚠️ Seleziona almeno una chance.")
        return

    user_id_phase[user_id] = PHASE_PLAY

    bot.send_message(
        call.message.chat.id,
        f"✅ Chances confermate: {', '.join(chances)}.\nPuoi ora iniziare a giocare.",
        reply_markup=get_main_keyboard()
    )
