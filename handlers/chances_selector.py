from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from logic.state import selected_chances
from messages.keyboard import get_main_keyboard

ALL_CHANCES = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]
SUGGESTED = []  # Se vuoi pre-impostare dei suggeriti da altra logica

def show_chances_selection(bot, message: Message, suggested=None):
    user_id = message.from_user.id
    selected_chances[user_id] = []

    markup = InlineKeyboardMarkup(row_width=3)
    buttons = []

    for ch in ALL_CHANCES:
        emoji = "✅" if ch in SUGGESTED else "➖"
        buttons.append(InlineKeyboardButton(f"{emoji} {ch}", callback_data=f"chance:{ch}"))

    # Aggiunta bottoni chances in due righe
    for i in range(0, len(buttons), 3):
        markup.row(*buttons[i:i+3])

    # Bottone conferma
    markup.add(InlineKeyboardButton("🎯 Conferma e inizia il gioco", callback_data="conferma_chances"))

    suggerite_txt = ", ".join(SUGGESTED) if SUGGESTED else "nessuna"
    bot.send_message(
        message.chat.id,
        f"🔍 *Suggerite:* {suggerite_txt}\n\nScegli le chances che vuoi usare:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

def handle_chance_callbacks(bot: object):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("chance:"))
    def select_chance(call: CallbackQuery):
        ch = call.data.split(":")[1]
        user_id = call.from_user.id

        if user_id not in selected_chances:
            selected_chances[user_id] = []

        if ch in selected_chances[user_id]:
            selected_chances[user_id].remove(ch)
        else:
            selected_chances[user_id].append(ch)

        show_chances_selection(bot, call.message)

    @bot.callback_query_handler(func=lambda call: call.data == "conferma_chances")
    def conferma_chances(call: CallbackQuery):
        user_id = call.from_user.id
        scelte = selected_chances.get(user_id, [])

        if not scelte:
            bot.answer_callback_query(call.id, "⚠️ Seleziona almeno una chance.")
            return

        bot.send_message(
            call.message.chat.id,
            f"🎮 Inizio gioco con chances: *{', '.join(scelte)}*",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
        # Qui puoi eventualmente far partire la FASE GIOCO

        # Pulisci callback
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
