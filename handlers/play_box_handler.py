# handlers/play_box_handler.py
from telebot.types import Message
from logic.state import selected_chances
from logic.game import get_next_bets, update_boxes
from messages.keyboard import get_numeric_keyboard

user_history = {}


def register(bot):
    @bot.message_handler(func=lambda msg: msg.text.isdigit() and 0 <= int(msg.text) <= 36)
    def handle_play_input(message: Message):
        chat_id = message.chat.id
        numero = int(message.text)

        chances = selected_chances.get(chat_id, [])
        if not chances:
            bot.send_message(chat_id, "⚠️ Devi prima confermare le chances attive.")
            return

        # Salva cronologia (per Annulla o Statistiche in futuro)
        if chat_id not in user_history:
            user_history[chat_id] = []
        user_history[chat_id].append(numero)

        # Calcolo vincite
        vincite = []
        if numero == 0:
            vincite = []
        else:
            if numero % 2 == 0:
                vincite.append("Pari")
            else:
                vincite.append("Dispari")
            if numero >= 1 and numero <= 18:
                vincite.append("Manque")
            elif numero >= 19:
                vincite.append("Passe")
            if numero in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]:
                vincite.append("Rosso")
            else:
                vincite.append("Nero")

        update_boxes(chat_id, vincite)
        next_bets = get_next_bets(chat_id)

        msg = f"🎯 Numero uscito: *{numero}*\n\n"
        msg += "🎰 *Chances vincenti:* " + (", ".join(vincite) if vincite else "Nessuna") + "\n\n"
        msg += "🎯 *Prossime fiches da puntare:*\n"
        for ch, val in next_bets.items():
            msg += f"• {ch}: {val}\n"

        bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=get_numeric_keyboard())
