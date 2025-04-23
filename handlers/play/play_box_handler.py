# handlers/play/play_box_handler.py
from telebot.types import Message
from logic.state import user_data
from logic.game import get_next_bets, update_boxes
from messages.keyboard import get_main_keyboard


def register(bot):
    @bot.message_handler(func=lambda m: m.text.isdigit())
    def handle_game_input(message: Message):
        chat_id = message.chat.id
        numero = int(message.text)

        if chat_id not in user_data or not user_data[chat_id].get("selected_chances"):
            bot.send_message(chat_id, "⚠️ Prima devi selezionare le chances tramite Analisi o Avvio rapido.", reply_markup=get_main_keyboard())
            return

        # Aggiungi numero alla lista
        user_data[chat_id]["numbers"].append(numero)

        # Ottieni chances attive e boxes
        chances = user_data[chat_id]["selected_chances"]
        boxes = user_data[chat_id]["user_boxes"]

        # Calcola fiches da puntare e aggiorna stato
        next_bets = get_next_bets(boxes)
        update_boxes(boxes, numero, chances)

        # Costruisci messaggio
        bets_text = "\n".join([f"➡️ *{chance}*: {fiches} fiche" for chance, fiches in next_bets.items()])
        msg = (
            f"🎯 Numero uscito: *{numero}*\n\n"
            f"🎯 *Prossime fiches da puntare:*\n{bets_text}\n\n"
            f"📈 Totale estrazioni: {len(user_data[chat_id]['numbers'])}"
        )

        bot.send_message(chat_id, msg, parse_mode="Markdown")
