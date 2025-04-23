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
