# handlers/play/start_handler.py
from telebot.types import Message
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        welcome_text = """🎰 *Benvenuto su ChanceTracker!*

Questo bot ti aiuterà a seguire la tua strategia alla roulette con il sistema a box.

🔍 *Analizza* – Inserisci 10-20 numeri per ottenere i suggerimenti sulle chances più attive.

⚡ *Avvio rapido* – Salta l’analisi e scegli direttamente le chances da attivare.

🎮 Dopo la selezione delle chances, partirà la fase di gioco con gestione automatica dei box.

☰ Puoi sempre aprire il *Menu* per usare le funzioni extra come:
↩️ Annulla – per correggere
📊 Statistiche – per monitorare l’andamento
♻️ Reset – per ricominciare

🍀 Buona fortuna e buon divertimento!
"""
        bot.send_message(
            message.chat.id,
            welcome_text,
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
