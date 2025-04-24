# ✅ handlers/play/play_box_handler.py

from telebot.types import Message
from logic.state import user_id_phase, PHASE_PLAY, selected_chances
from logic.game import get_next_bet, update_boxes
from messages.keyboard import get_numeric_keyboard, get_main_keyboard

def register(bot):
    @bot.message_handler(func=lambda message: user_id_phase.get(message.from_user.id) == PHASE_PLAY)
    def handle_game_number(message: Message):
        user_id = message.from_user.id
        numero = int(message.text)

        # Logica semplificata di vincita (adatta alla tua strategia reale)
        winning_chances = []
        if numero % 2 == 0:
            winning_chances.append("Pari")
        else:
            winning_chances.append("Dispari")

        if numero <= 18:
            winning_chances.append("Manque")
        else:
            winning_chances.append("Passe")

        if numero == 0:
            winning_chances = []

        update_boxes(user_id, winning_chances)
        bets = get_next_bet(user_id)

        text = "🎯 *Numero uscito:* `{}`\n".format(numero)
        text += "\n🎰 *Risultati del turno:*\n"
        for chance, bet in bets.items():
            result = "✅ Vinta" if chance in winning_chances else "❌ Persa"
            text += f"• {chance}: {bet} fiche – {result}\n"

        text += "\n🎲 *Prossime fiches da puntare:*\n"
        for chance, bet in bets.items():
            text += f"• {chance}: {bet} fiche\n"

        bot.send_message(
            message.chat.id,
            text,
            parse_mode='Markdown',
            reply_markup=get_numeric_keyboard()
        )
