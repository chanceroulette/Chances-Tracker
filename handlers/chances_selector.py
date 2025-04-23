from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.analysis import analyze_chances
from logic.state import selected_chances, user_boxes
from messages.keyboard import get_main_keyboard, get_number_keyboard
from logic.game import initialize_boxes

# Mostra selezione chances
def show_chances_selection(bot, chat_id, numbers):
    suggerite = []
    if numbers:
        suggerite = analyze_chances(numbers)

    # Salva suggerite per selezione iniziale
    selected_chances[chat_id] = suggerite.copy()

    markup = InlineKeyboardMarkup(row_width=2)
    for chance in ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]:
        prefix = "✅ " if chance in suggerite else "⬜️ "
        markup.add(InlineKeyboardButton(f"{prefix}{chance}", callback_data=f"toggle_{chance}"))

    markup.add(InlineKeyboardButton("🎯 Conferma e inizia il gioco", callback_data="conferma_chances"))

    suggerite_msg = (
        f"🔍 *Suggerite:* {', '.join(suggerite) if suggerite else 'nessuna'}\n"
        f"Scegli le chances che vuoi usare:"
    )
    bot.send_message(chat_id, suggerite_msg, parse_mode="Markdown", reply_markup=markup)


# Gestione selezione e conferma
def handle_chance_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_"))
    def toggle_chance(call):
        user_id = call.from_user.id
        chance = call.data.replace("toggle_", "")

        if user_id not in selected_chances:
            selected_chances[user_id] = []

        if chance in selected_chances[user_id]:
            selected_chances[user_id].remove(chance)
        else:
            selected_chances[user_id].append(chance)

        # Ricostruisce la tastiera aggiornata
        markup = InlineKeyboardMarkup(row_width=2)
        for c in ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]:
            prefix = "✅ " if c in selected_chances[user_id] else "⬜️ "
            markup.add(InlineKeyboardButton(f"{prefix}{c}", callback_data=f"toggle_{c}"))
        markup.add(InlineKeyboardButton("🎯 Conferma e inizia il gioco", callback_data="conferma_chances"))

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == "conferma_chances")
    def conferma(call):
        user_id = call.from_user.id

        if user_id not in selected_chances or len(selected_chances[user_id]) == 0:
            bot.answer_callback_query(call.id, "❗ Seleziona almeno una chance")
            return

        chances = selected_chances[user_id]
        user_boxes[user_id] = initialize_boxes(chances)

        messaggio = (
            f"✅ Chances attive: *{', '.join(chances)}*\n"
            f"🎯 Inizia il gioco! Inserisci il numero uscito alla roulette."
        )

        bot.send_message(
            call.message.chat.id,
            messaggio,
            parse_mode="Markdown",
            reply_markup=get_number_keyboard()
        )
