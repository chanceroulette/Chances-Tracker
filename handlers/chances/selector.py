from telebot.types import Message
from logic.state import suggested_chances, selected_chances, user_id_phase
from messages.keyboard_chances import get_chances_keyboard
from messages.keyboard import get_main_keyboard
from logic.game import initialize_boxes

def show_chances_selection(bot, message: Message, suggested):
    user_id = message.from_user.id
    suggested_chances[user_id] = suggested
    selected_chances[user_id] = set(suggested)  # Selezionate di default

    msg = (
        f"🔍 *Suggerite:* {', '.join(suggested)}\n"
        f"_Puoi selezionare o deselezionare le chances che preferisci._\n"
        f"⬇️ Conferma per continuare"
    )

    bot.send_message(
        message.chat.id,
        msg,
        parse_mode='Markdown',
        reply_markup=get_chances_keyboard(suggested)
    )

def handle_chance_callbacks(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("chance_"))
    def select_chance(call):
        user_id = call.from_user.id
        chance = call.data.replace("chance_", "")

        if user_id not in selected_chances:
            selected_chances[user_id] = set()

        if chance in selected_chances[user_id]:
            selected_chances[user_id].remove(chance)
        else:
            selected_chances[user_id].add(chance)

        keyboard = get_chances_keyboard(suggested_chances.get(user_id, []))
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )

    @bot.callback_query_handler(func=lambda call: call.data == "confirm_chances")
    def confirm_chances(call):
        user_id = call.from_user.id
        chances = selected_chances.get(user_id, set())

        if not chances:
            bot.answer_callback_query(call.id, "⚠️ Seleziona almeno una chance.")
            return

        initialize_boxes(user_id, chances)
        user_id_phase[user_id] = "game"

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=(
                f"✅ Chances attive: *{', '.join(chances)}*\n"
                f"🎯 Ora puoi iniziare il gioco con i box.\n\n"
                f"Inserisci il primo numero uscito oppure premi ☰ Menu",
            ),
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
