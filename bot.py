import os
from dotenv import load_dotenv
from flask import Flask, request
import telebot

# Carica le variabili d’ambiente
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)

# Import dei moduli handlers
from handlers import (
    start_handler,
    play_handler,
    undo_handler,
    reset_handler,
    menu_handler,
    help_handler,
    stats_handler,
    chances_selector  # Ora nella cartella handlers
)

# Registrazione di tutti i comandi
start_handler.register(bot)
play_handler.register(bot)
undo_handler.register(bot)
reset_handler.register(bot)
menu_handler.register(bot)
help_handler.register(bot)
stats_handler.register(bot)
chances_selector.register(bot)

# Webhook setup
import requests

# Controlla se il webhook è già impostato
r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo")
current_url = r.json()["result"].get("url", "")

if current_url != WEBHOOK_URL:
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print("🔁 Webhook aggiornato all’avvio")
else:
    print("✅ Webhook già attivo")

# Flask app per ricezione webhook
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Bot attivo (GET test)"

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == '__main__':
    print("🤖 Flask in ascolto...")
    app.run(host='0.0.0.0', port=10000)
