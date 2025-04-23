import os
from flask import Flask, request
from telebot import TeleBot
from telebot.types import Update

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = TeleBot(TOKEN)

# HANDLER IMPORTS
from handlers import (
    start_handler,
    play_handler,
    undo_handler,
    reset_handler,
    help_handler,
    menu_handler,
    stats_handler,
    chances_selector  # ✅ aggiunto
)

# REGISTRA HANDLER
start_handler.register(bot)
play_handler.register(bot)
undo_handler.register(bot)
reset_handler.register(bot)
help_handler.register(bot)
menu_handler.register(bot)
stats_handler.register(bot)

# ✅ Attiva gestione dei callback per la selezione chances
chances_selector.handle_chance_callbacks(bot)

# FLASK SETUP
app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return "🤖 Bot attivo (GET)"

@app.route('/', methods=['POST'])
def webhook():
    update = Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return '', 200

# IMPOSTAZIONE WEBHOOK ALL'AVVIO
def set_webhook():
    import requests
    info = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo").json()
    current = info["result"].get("url", "")

    if current != WEBHOOK_URL:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
        print("🔁 Webhook aggiornato all’avvio")
    else:
        print("✅ Webhook già attivo")

if __name__ == '__main__':
    set_webhook()
    print("🤖 Flask in ascolto...")
    app.run(host='0.0.0.0', port=10000)
