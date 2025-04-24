from telebot.types import Message
from messages.keyboard_generale import get_main_keyboard

def handle_menu(bot, message: Message):
    bot.send_message(
        message.chat.id,
        "📋 *Menu principale:*\n\n"
        "• 🎲 Avvio rapido — entra subito in modalità gioco\n"
        "• 🧮 Analizza — suggerisce le migliori chances\n"
        "• 📊 Statistiche — (in arrivo)\n"
        "• ↩️ Annulla — annulla l’ultima azione\n"
        "• 🔄 Reset — resetta tutto\n",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
