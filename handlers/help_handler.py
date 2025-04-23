# handlers/play/help_handler.py

def register(bot):
    @bot.message_handler(commands=['help'])
    def send_help(message):
        text = (
            "ℹ️ *Aiuto - Comandi disponibili*\n\n"
            "*🎯 Fase di Analisi:*\n"
            "- 🧮 Analizza: inserisci numeri per trovare le chances migliori.\n"
            "- ⚡ Avvio rapido: scegli manualmente le chances.\n\n"
            "*🎲 Fase di Gioco:*\n"
            "- 🎯 Gioca: inizia a giocare con le chances selezionate.\n"
            "- ↩️ Annulla: annulla l'ultima operazione.\n"
            "- 🔄 Reset: resetta la sessione.\n"
            "- 📊 Statistiche: mostra statistiche della sessione."
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown")


# handlers/play/menu_handler.py
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "☰ Menu")
    def show_menu(message):
        text = (
            "🔍 *Menu Principale*\n\n"
            "🔮 *Fase Analisi*\n"
            "📊 Analizza – inserisci numeri per analisi automatica\n"
            "⚡ Avvio rapido – scegli direttamente le chances\n\n"
            "🎢 *Fase di Gioco*\n"
            "🎲 Gioca – avvia la strategia con sistema a box\n"
            "↩️ Annulla • 🔄 Reset • 📊 Statistiche\n\n"
            "_Tocca un tasto qui sotto per iniziare 👇_"
        )
        bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=get_main_keyboard())


# handlers/play/start_handler.py
from messages.welcome import get_welcome_message
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.send_message(
            message.chat.id,
            get_welcome_message(),
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
