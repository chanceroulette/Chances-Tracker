import os
from dotenv import load_dotenv
from flask import Flask, request
import telebot
import requests

# Carica variabili d'ambiente
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)

# Import dei vari handler standard
from handlers import (
    start_handler,
    play_handler,
    undo_handler,
    reset_handler,
    menu_handler,
    help_handler,
    stats_handler
)

# Import callback handler per i pulsanti inline (chances)
from handlers.chances_selector import handle_chance_callbacks

# Registrazione di tutti i comandi base
start_handler.register(bot)
play_handler.register(bot)
undo_handler.register(bot)
reset_handler.register(bot)
menu_handler.register(bot)
help_handler.register(bot)
stats_handler.register(bot)

# ✅ Registrazione gestore per callback inline (chances)
bot.register_callback_query_handler(handle_chance_callbacks, func=lambda call: True)

# Webhook: imposta se diverso da quello attuale
r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo")
current_url = r.json()["result"].get("url", "")

if current_url != WEBHOOK_URL:
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print("🔁 Webhook aggiornato all’avvio")
else:
    print("✅ Webhook già attivo")

# Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "🤖 Bot attivo e funzionante!"

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == '__main__':
    print("🚀 Flask in ascolto...")
    app.run(host='0.0.0.0', port=10000)
