from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.state import selected_chances, game_phase, user_boxes
from logic.game import initialize_boxes
from messages.keyboard import get_main_keyboard

# Lista completa delle 6 chances semplici
ALL_CHANCES = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]

# Mostra tastiera di selezione delle chances
def show_chances_selection(bot, chat_id, user_id, suggerite):
    markup = InlineKeyboardMarkup(row_width=2)
    for chance in ALL_CHANCES:
        label = f"✅ {chance}" if chance in suggerite else chance
        markup.add(InlineKeyboardButton(label, callback_data=f"chance:{chance}"))

    markup.add(InlineKeyboardButton("🎯 Conferma e inizia il gioco", callback_data="conferma"))

    msg = (
        f"🔍 *Suggerite:* {', '.join(suggerite)}\n\n"
        "Seleziona le chances su cui vuoi giocare. Puoi scegliere anche diverse da quelle suggerite."
    )
    bot.send_message(chat_id, msg, parse_mode='Markdown', reply_markup=markup)

# Gestione callback dei bottoni

def handle_chance_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("chance:"))
    def toggle_chance(call):
        user_id = call.from_user.id
        chance = call.data.split(":")[1]
        selected = selected_chances.setdefault(user_id, set())

        if chance in selected:
            selected.remove(chance)
        else:
            selected.add(chance)

        # Ricarica la tastiera aggiornata
        markup = InlineKeyboardMarkup(row_width=2)
        for ch in ALL_CHANCES:
            label = f"✅ {ch}" if ch in selected else ch
            markup.add(InlineKeyboardButton(label, callback_data=f"chance:{ch}"))

        markup.add(InlineKeyboardButton("🎯 Conferma e inizia il gioco", callback_data="conferma"))

        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == "conferma")
    def confirm_selection(call):
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        selected = selected_chances.get(user_id, set())

        if not selected:
            bot.answer_callback_query(call.id, "⚠️ Seleziona almeno una chance.", show_alert=True)
            return

        initialize_boxes(user_id, selected)
        game_phase[user_id] = "gioco"

        bot.send_message(
            chat_id,
            f"🎮 *Gioco iniziato!* Chances attive: {', '.join(selected)}",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
