# bot.py
import os
from dotenv import load_dotenv
from flask import Flask, request
import telebot

from handlers import (
    start_handler,
    menu_handler,
    stats_handler,
    undo_handler,
    reset_handler,
    play_box_handler,
    analyze_handler,
)

from handlers.chances import selector

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Registrazione dei comandi
start_handler.register(bot)
menu_handler.register(bot)
stats_handler.register(bot)
undo_handler.register(bot)
reset_handler.register(bot)
play_box_handler.register(bot)
analyze_handler.register(bot)
selector.register(bot)

# Webhook Flask
@app.route('/', methods=['GET'])
def index():
    return "Bot attivo!", 200

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

# Rimuove webhook precedente e imposta quello nuovo
bot.remove_webhook()
bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
print("🔁 Webhook aggiornato all’avvio")
print("🚀 Avvio Flask...")

# Avvia Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
