# handlers/play/menu_handler.py
from telebot.types import Message
from messages.keyboard import get_main_keyboard


def register(bot):
    @bot.message_handler(commands=["menu"])
    def show_menu(message: Message):
        text = (
            "🧭 *Menu Principale*\n\n"
            "🔍 *Fase Analisi*\n"
            "• 📊 Analizza – inserisci numeri per analisi automatica\n"
            "• ⚡ Avvio rapido – scegli direttamente le chances\n\n"
            "🎯 *Fase di Gioco*\n"
            "• 🎲 Gioca – avvia la strategia con sistema a box\n"
            "• ↩️ Annulla – ♻️ Reset – 📊 Statistiche\n\n"
            "_Tocca un tasto qui sotto per iniziare 👇_"
        )
        bot.send_message(
            message.chat.id,
            text,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
