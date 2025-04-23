from telebot.types import CallbackQuery
from logic.state import selected_chances, user_id_phase, PHASE_PLAY
from messages.keyboard import get_main_keyboard
from handlers.chances.selector import get_chance_markup
from logic.game import initialize_boxes


def register(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("chance_"))
    def select_chance(call: CallbackQuery):
        user_id = call.from_user.id
        chance = call.data.split("_")[1]

        if chance in selected_chances[user_id]:
            selected_chances[user_id].remove(chance)
        else:
            selected_chances[user_id].append(chance)

        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_chance_markup(user_id)
        )

    @bot.callback_query_handler(func=lambda call: call.data == "confirm_chances")
    def confirm_chances(call: CallbackQuery):
        user_id = call.from_user.id
        chances = selected_chances.get(user_id, [])

        if not chances:
            bot.answer_callback_query(call.id, "⚠️ Seleziona almeno una chance.")
            return

        initialize_boxes(user_id, chances)
        user_id_phase[user_id] = PHASE_PLAY

        bot.send_message(
            call.message.chat.id,
            f"✅ Chances attive: *{', '.join(chances)}*

🎯 Inizia la FASE GIOCO inserendo i numeri estratti!",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
