from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from logic.state import selected_chances, user_boxes
from logic.game import initialize_boxes
from messages.keyboard import get_main_keyboard

CHANCES = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]

# Mostra la selezione delle chances suggerite o libere
def show_chances_selection(bot, chat_id, suggerite=None):
    suggerite = suggerite or []
    selected_chances[chat_id] = []

    text = "\ud83d\udd0d *Suggerite:* "
    if suggerite:
        text += ", ".join(suggerite)
    else:
        text += "nessuna"
    text += "\n\nScegli le chances che vuoi usare:"

    markup = build_chance_keyboard(chat_id, suggerite)
    bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=markup)

# Costruzione tastiera dinamica

def build_chance_keyboard(chat_id, suggerite):
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = []
    for chance in CHANCES:
        label = f"\u2705 {chance}" if chance in selected_chances[chat_id] else chance
        if chance in suggerite:
            label = f"\u25FB {label}"
        buttons.append(InlineKeyboardButton(label, callback_data=f"toggle_{chance}"))
    for i in range(0, len(buttons), 3):
        markup.row(*buttons[i:i+3])
    markup.row(InlineKeyboardButton("\ud83c\udfaf Conferma e inizia il gioco", callback_data="conferma_chances"))
    return markup

# Callback

def handle_chance_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_") or call.data == "conferma_chances")
    def handle_callback(call: CallbackQuery):
        chat_id = call.message.chat.id

        if chat_id not in selected_chances:
            selected_chances[chat_id] = []

        if call.data.startswith("toggle_"):
            chance = call.data.split("_")[1]
            if chance in selected_chances[chat_id]:
                selected_chances[chat_id].remove(chance)
            else:
                selected_chances[chat_id].append(chance)

            markup = build_chance_keyboard(chat_id, [])
            bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=markup)

        elif call.data == "conferma_chances":
            if not selected_chances[chat_id]:
                bot.answer_callback_query(call.id, "Seleziona almeno una chance.", show_alert=True)
                return

            # Inizializza i box di gioco
            user_boxes[chat_id] = initialize_boxes(selected_chances[chat_id])

            bot.edit_message_text(
                chat_id=chat_id,
                message_id=call.message.message_id,
                text="✅ Chances selezionate. Il gioco è pronto! Usa il comando 🎲 *Gioca* per iniziare.",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )
