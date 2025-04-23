from telebot.types import Message
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(commands=["menu"])
    @bot.message_handler(func=lambda message: message.text == "☰ Menu")
    def show_menu(message: Message):
        bot.send_message(
            message.chat.id,
            "🧭 *Menu Principale*\n\n"
            "🔍 *Fase Analisi*\n"
            "• 📊 Analizza – inserisci numeri per analisi automatica\n"
            "• ⚡ Avvio rapido – scegli direttamente le chances\n\n"
            "🎯 *Fase di Gioco*\n"
            "• 🎲 Gioca – avvia la strategia con sistema a box\n"
            "• ↩️ Annulla • 📊 Statistiche • 🔄 Reset\n\n"
            "_Tocca un tasto qui sotto per iniziare 👇_",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
