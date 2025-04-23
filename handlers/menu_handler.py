from telebot.types import Message
from telebot import types
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(commands=["menu"])
    @bot.message_handler(func=lambda message: message.text == "☰ Menu")
    def show_menu(message: Message):
        try:
            with open("assets/welcome_image.png", "rb") as photo:
                bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=(
                        "🧭 *Menu Principale*\n\n"
                        "• 🎲 *Gioca* – Inserisci i numeri e attiva il sistema\n"
                        "• ↩️ *Annulla* – Ripristina l’ultima giocata\n"
                        "• 📊 *Statistiche* – Controlla i tuoi risultati\n"
                        "• 🔄 *Reset* – Azzeramento completo della sessione\n\n"
                        "_Scegli un'opzione dalla tastiera qui sotto_ 👇"
                    ),
                    parse_mode='Markdown',
                    reply_markup=get_main_keyboard()
                )
        except Exception as e:
            bot.send_message(
                message.chat.id,
                "⚠️ Impossibile caricare l'immagine del menu.\n"
                f"Errore: `{str(e)}`",
                parse_mode='Markdown'
            )
