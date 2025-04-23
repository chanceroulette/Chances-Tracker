# handlers/chances/callbacks.py
from telebot.types import CallbackQuery
from logic.state import selected_chances
from handlers.chances.selector import get_chance_markup
from logic.game import initialize_boxes

ALL_CHANCES = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]

def register(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_"))
    def toggle_chance(call: CallbackQuery):
        chat_id = call.message.chat.id
        chance = call.data.split("_", 1)[1]
        if chat_id not in selected_chances:
            selected_chances[chat_id] = set()

        if chance in selected_chances[chat_id]:
            selected_chances[chat_id].remove(chance)
        else:
            selected_chances[chat_id].add(chance)

        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=get_chance_markup(chat_id))

    @bot.callback_query_handler(func=lambda call: call.data == "confirm_chances")
    def confirm_chances(call: CallbackQuery):
        chat_id = call.message.chat.id
        chances = list(selected_chances.get(chat_id, []))
        if not chances:
            bot.answer_callback_query(call.id, "❗ Seleziona almeno una chance.", show_alert=True)
            return

        initialize_boxes(chat_id, chances)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"✅ Chances attive: *{', '.join(chances)}*\nInizia ora la fase di gioco.",
            parse_mode="Markdown"
        )
        # (Aggiungeremo qui la transizione alla fase 3: gioco)
