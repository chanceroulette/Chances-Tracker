# handlers/play/help_handler.py
from telebot.types import Message
from messages.keyboard import get_main_keyboard


def register(bot):
    @bot.message_handler(commands=["help"])
    def help_command(message: Message):
        bot.send_message(
            message.chat.id,
            "ℹ️ *Guida Rapida*

"
            "• /start – Mostra il messaggio di benvenuto
"
            "• 🎲 Gioca – Inserisci numeri e attiva la strategia
"
            "• 📊 Statistiche – Visualizza i dati della sessione
"
            "• ↩️ Annulla – Annulla l’ultima giocata
"
            "• ♻️ Reset – Resetta tutta la sessione
"
            "• ☰ Menu – Ritorna al menu principale",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
