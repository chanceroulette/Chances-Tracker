from telebot.types import Message
from logic.state import selected_chances, user_boxes
from logic.game import get_next_bet, update_boxes
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(func=lambda message: message.text.isdigit() and 0 <= int(message.text) <= 36)
    def play_turn(message: Message):
        user_id = message.from_user.id
        if user_id not in selected_chances or user_id not in user_boxes:
            bot.send_message(message.chat.id, "⚠️ Devi prima avviare il gioco selezionando le chances.", reply_markup=get_main_keyboard())
            return

        numero = int(message.text)
        attive = selected_chances[user_id]
        boxes_dict = user_boxes[user_id]

        # Determina vincite
        outcomes = {}
        for chance in attive:
            outcomes[chance] = is_win(chance, numero)

        # Calcola fiches giocate
        puntate = get_next_bet(boxes_dict)
        vincite = {ch: sum(puntate[ch]) if outcomes[ch] else 0 for ch in attive}
        perdite = {ch: sum(puntate[ch]) if not outcomes[ch] else 0 for ch in attive}

        # Aggiorna i box
        user_boxes[user_id] = update_boxes(boxes_dict, outcomes)

        # Risultato testuale
        msg = (
            f"🎯 Numero uscito: *{numero}*

"
        )
        for ch in attive:
            msg += (
                f"• *{ch}* → {'✅ Vinto' if outcomes[ch] else '❌ Perso'} | "
                f"Puntate: `{sum(puntate[ch])}` | "
                f"{'Vincita' if outcomes[ch] else 'Perdita'}: `{vincite[ch] or perdite[ch]}`
"
            )

        bot.send_message(message.chat.id, msg, parse_mode='Markdown', reply_markup=get_main_keyboard())

def is_win(chance, number):
    if chance == "Rosso":
        return number in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    if chance == "Nero":
        return number in [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
    if chance == "Pari":
        return number != 0 and number % 2 == 0
    if chance == "Dispari":
        return number % 2 == 1
    if chance == "Manque":
        return 1 <= number <= 18
    if chance == "Passe":
        return 19 <= number <= 36
    return False
