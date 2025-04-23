from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.state import selected_chances, confirmed_chances
from messages.keyboard import get_main_keyboard

ALL_CHANCES = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]

def show_chances_selection(bot, chat_id, suggestions=None):
    user_id = chat_id  # lo user_id coincide in questo contesto
    markup = InlineKeyboardMarkup(row_width=3)
    if user_id not in selected_chances:
        selected_chances[user_id] = suggestions if suggestions else []

    buttons = []
    for chance in ALL_CHANCES:
        selected = chance in selected_chances[user_id]
        emoji = "✅" if selected else "➖"
        buttons.append(InlineKeyboardButton(f"{emoji} {chance}", callback_data=f"toggle_{chance}"))

    markup.add(*buttons)
    markup.add(InlineKeyboardButton("🎯 Conferma e inizia il gioco", callback_data="confirm_chances"))
    bot.send_message(
        chat_id,
        f"🔍 *Suggerite:* {', '.join(suggestions) if suggestions else 'nessuna'}\n\nScegli le chances che vuoi usare:",
        parse_mode='Markdown',
        reply_markup=markup
    )

def handle_chance_callbacks(bot, call):
    user_id = call.from_user.id
    if user_id not in selected_chances:
        selected_chances[user_id] = []

    if call.data.startswith("toggle_"):
        chance = call.data.replace("toggle_", "")
        if chance in selected_chances[user_id]:
            selected_chances[user_id].remove(chance)
        else:
            selected_chances[user_id].append(chance)
        show_chances_selection(bot, call.message.chat.id, suggestions=[])
    
    elif call.data == "confirm_chances":
        confirmed_chances[user_id] = selected_chances.get(user_id, [])
        bot.send_message(
            call.message.chat.id,
            f"🎮 *Chances selezionate:* {', '.join(confirmed_chances[user_id])}",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
