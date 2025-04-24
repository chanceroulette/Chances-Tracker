from telebot.types import Message
from logic.state import user_id_phase, PHASE_PLAY
from logic.game import get_next_bet, update_boxes
from messages.keyboard import get_numeric_keyboard, get_main_keyboard


def register(bot):
    @bot.message_handler(func=lambda m: user_id_phase.get(m.from_user.id) == PHASE_PLAY and m.text.isdigit())
    def handle_play_number(message: Message):
        user_id = message.from_user.id
        numero = int(message.text)

        # Calcolo delle puntate da effettuare
        bets = get_next_bet(user_id)

        msg = f"🎯 Numero uscito: *{numero}*\n\n"
        msg += "🎲 Puntate da effettuare:\n"

        for chance, bet in bets.items():
            msg += f"• `{chance}`: {bet} fiches\n"

        # Aggiorna i box in base all'esito del numero
        update_boxes(user_id, numero)

        bot.send_message(
            message.chat.id,
            msg,
            parse_mode='Markdown',
            reply_markup=get_numeric_keyboard()
        )
