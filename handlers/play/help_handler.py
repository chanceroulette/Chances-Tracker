# handlers/play/help_handler.py
from telebot.types import Message

def register(bot):
    @bot.message_handler(commands=['help'])
    def help_command(message: Message):
        bot.send_message(
            message.chat.id,
            """ℹ️ *Guida al Bot*

Usa questo bot per simulare un sistema strategico di gioco alla roulette europea.

*Fasi principali:*
1. 📈 *Analisi*: inserisci i numeri usciti per ricevere suggerimenti sulle chances migliori.
2. ⚡️ *Avvio rapido*: seleziona manualmente le chances che preferisci.
3. 🎲 *Gioco*: inserisci i numeri della roulette e segui la strategia a box.

Comandi utili:
/start – Riavvia il bot
/analizza – Inserisci numeri per l'analisi
/gioca – Avvia il gioco
/reset – Resetta la sessione
/statistiche – Mostra l'andamento della sessione
/annulla – Annulla l'ultima giocata
/help – Mostra questo messaggio

""",
            parse_mode="Markdown"
        )
