import os
import telebot
from flask import Flask, request
from dotenv import load_dotenv

from handlers import (
    start_handler,
    menu_handler,
    undo_handler,
    reset_handler,
    stats_handler,
    analyze_handler,
    chances_selector,
    play_box_handler
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')
app = Flask(__name__)

# Webhook route
@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return '', 403

# Registro handler
start_handler.register(bot)
menu_handler.register(bot)
undo_handler.register(bot)
reset_handler.register(bot)
stats_handler.register(bot)
analyze_handler.register(bot)
play_box_handler.register(bot)

# Callback query per chances
chances_selector.handle_chance_callbacks(bot)

# Imposta webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)
print("🔁 Webhook aggiornato all’avvio")

# Avvia Flask
print("🚀 Avvio Flask...")
app.run(host="0.0.0.0", port=10000)
