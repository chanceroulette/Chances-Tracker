from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from logic.analysis import analyze_chances
from logic.state import selected_chances, user_boxes
from logic.game import initialize_boxes
from messages.keyboard import get_main_keyboard

# Mostra tastiera di selezione chances

def show_chances_selection(bot, chat_id, numbers):
    suggerite = analyze_chances(numbers)
    selected_chances[chat_id] = suggerite.copy()

    text = (
        f"🔍 *Suggerite:* {', '.join(suggerite)}\n"
        "Puoi selezionare o deselezionare liberamente le chances da usare.\n"
        "Premi ✅ *Conferma* per iniziare la fase di gioco."
    )

    keyboard = InlineKeyboardMarkup()
    row = []
    for chance in ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]:
        selected = "✅" if chance in selected_chances[chat_id] else "⬜"
        row.append(InlineKeyboardButton(f"{selected} {chance}", callback_data=f"toggle_{chance}"))
        if len(row) == 2:
            keyboard.row(*row)
            row = []
    if row:
        keyboard.row(*row)

    keyboard.row(InlineKeyboardButton("✅ Conferma", callback_data="conferma_chances"))

    bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# Gestione callback chance

def handle_chance_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_"))
    def toggle_chance(call: CallbackQuery):
        user_id = call.message.chat.id
        chance = call.data.replace("toggle_", "")
        if user_id not in selected_chances:
            selected_chances[user_id] = []

        if chance in selected_chances[user_id]:
            selected_chances[user_id].remove(chance)
        else:
            selected_chances[user_id].append(chance)

        bot.answer_callback_query(call.id)
        show_chances_selection(bot, user_id, [])

    @bot.callback_query_handler(func=lambda call: call.data == "conferma_chances")
    def conferma_chances(call: CallbackQuery):
        user_id = call.message.chat.id
        chances = selected_chances.get(user_id, [])

        if not chances:
            bot.answer_callback_query(call.id, "❗ Seleziona almeno una chance.", show_alert=True)
            return

        initialize_boxes(user_id, chances)
        bot.send_message(
            user_id,
            "🎮 Fase di gioco avviata! Inserisci i numeri con la tastiera numerica.",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
