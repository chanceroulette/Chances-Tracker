from telebot.types import Message
from logic.state import selected_chances, user_boxes, game_phase
from logic.game import update_boxes, get_next_bet
from messages.keyboard import get_main_keyboard


def register(bot):
    @bot.message_handler(func=lambda message: message.text == "🎲 Gioca" or (
        message.text.isdigit() and 0 <= int(message.text) <= 36 and game_phase.get(message.from_user.id) == "gioco"
    ))
    def handle_game_play(message: Message):
        user_id = message.from_user.id
        chat_id = message.chat.id

        if message.text == "🎲 Gioca":
            if chat_id not in selected_chances or chat_id not in user_boxes:
                bot.send_message(chat_id, "⚠️ Nessuna sessione di gioco attiva.", reply_markup=get_main_keyboard())
                return
            bets = get_next_bet(user_boxes[chat_id])
            text = "🎯 *Prossime fiches da puntare:*\n"
            for chance, value in bets.items():
                text += f"• {chance}: {value} fiche\n"
            bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=get_main_keyboard())
            return

        # Numero inserito nella fase di gioco
        numero = int(message.text)
        results = update_boxes(chat_id, numero)

        msg = (
            f"🎯 Numero uscito: *{numero}*\n\n"
            "🎰 *Risultati chances:*\n"
        )
        for chance, res in results["dettagli"].items():
            icon = "✅" if res == "vinto" else "❌"
            msg += f"{icon} {chance}: {res}\n"

        msg += f"\n💰 *Totale fiches:* +{results['vinti']} / -{results['persi']} → `∆ {results['delta']}`"

        bot.send_message(chat_id, msg, parse_mode='Markdown', reply_markup=get_main_keyboard())
