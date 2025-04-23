# handlers/play/help_handler.py
from telebot.types import Message
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(commands=['help'])
    def send_help(message: Message):
        help_text = (
            "ℹ️ *Guida Rapida*\n\n"
            "🎰 *ChanceTracker* è un assistente alla roulette basato su una strategia a box.\n\n"
            "🔍 *Analizza* — Inserisci 10-20 numeri e il bot suggerirà le chances più attive.\n"
            "⚡ *Avvio rapido* — Salta l’analisi e scegli subito le chances.\n\n"
            "🎯 *Gioca* — Dopo aver selezionato le chances, inizia la partita.\n"
            "↩️ *Annulla* — Ripristina l’ultimo numero inserito.\n"
            "♻️ *Reset* — Ricomincia una nuova sessione.\n"
            "📊 *Statistiche* — Consulta i dati della tua sessione.\n\n"
            "☰ *Menu* — Sempre accessibile per muoverti tra le funzioni.\n\n"
            "_Buon divertimento e gioca responsabilmente!_"
        )

        bot.send_message(
            message.chat.id,
            help_text,
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
