from telebot.types import Message
from logic.state import selected_chances, user_boxes
from logic.game import get_next_bet, update_boxes
from messages.keyboard import get_game_keyboard

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "🎲 Gioca")
    def play_round(message: Message):
        user_id = message.from_user.id

        # Fase 1: Controllo precondizioni
        if user_id not in selected_chances or not selected_chances[user_id]:
            bot.send_message(
                message.chat.id,
                "⚠️ Prima devi selezionare le chances tramite *Analizza* o *Avvio rapido*.",
                parse_mode='Markdown',
                reply_markup=get_game_keyboard()
            )
            return

        if user_id not in user_boxes or not user_boxes[user_id]:
            bot.send_message(
                message.chat.id,
                "⚠️ Il sistema a box non è stato inizializzato correttamente.",
                reply_markup=get_game_keyboard()
            )
            return

        # Fase 2: Generazione suggerimenti di puntata
        fiches = get_next_bet(user_id)
        text = "🎯 *Prossime fiches da puntare:*\n\n"
        for chance, valore in fiches.items():
            text += f"• `{valore}` fiches su *{chance}*\n"

        # Fase 3: Richiesta numero uscito (input dell'utente)
        bot.send_message(
            message.chat.id,
            text + "\n👉 Ora inserisci il *numero uscito* nella roulette (0-36).",
            parse_mode='Markdown',
            reply_markup=get_game_keyboard()
        )

    @bot.message_handler(func=lambda message: message.text.isdigit() and 0 <= int(message.text) <= 36)
    def handle_result(message: Message):
        user_id = message.from_user.id
        numero = int(message.text)

        if user_id not in selected_chances or user_id not in user_boxes:
            return  # fuori contesto

        risultati = update_boxes(user_id, numero)

        msg = f"🎯 Numero uscito: *{numero}*\n\n"
        msg += "💰 *Esito per ciascuna chance:*\n"
        totale = 0
        for chance, esito in risultati.items():
            fiches = esito['puntate']
            vincita = esito['vincita']
            net = vincita - fiches
            totale += net
            status = "✅" if vincita > 0 else "❌"
            msg += f"{status} {chance} — Puntate: `{fiches}`, Vincita: `{vincita}`, Netto: `{net}`\n"

        msg += f"\n📊 *Totale netto turno:* `{totale}` fiches"

        bot.send_message(
            message.chat.id,
            msg,
            parse_mode='Markdown',
            reply_markup=get_game_keyboard()
        )
