import os
from dotenv import load_dotenv
import telebot
from flask import Flask, request

from handlers import start_handler
from handlers import play_handler
from handlers import menu_handler
from handlers import help_handler

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
bot = telebot.TeleBot(TOKEN)

# Registrazione handler
start_handler.register(bot)
help_handler.register(bot)
menu_handler.register(bot)
play_handler.register(bot)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Bot attivo (GET)', 200

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Unsupported content type', 403

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print("🤖 Webhook impostato e Flask attivo")
    app.run(host="0.0.0.0", port=10000)
