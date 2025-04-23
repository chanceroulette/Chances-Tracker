import os
import requests
from dotenv import load_dotenv
import telebot
from flask import Flask, request

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)

# === Importa tutti gli handler ===
from handlers import (
    start_handler,
    help_handler,
    menu_handler,
    play_handler,
    undo_handler,
    reset_handler
)

# === Registra gli handler ===
start_handler.register(bot)
help_handler.register(bot)
menu_handler.register(bot)
play_handler.register(bot)
undo_handler.register(bot)
reset_handler.register(bot)

# === Imposta webhook subito ===
try:
    r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo")
    current_url = r.json()["result"].get("url", "")
    if current_url != WEBHOOK_URL:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
        print("🔁 Webhook aggiornato all’avvio")
    else:
        print("✅ Webhook già attivo all’avvio")
except Exception as e:
    print(f"❌ Errore durante il controllo webhook: {e}")

# === Flask per ricevere i messaggi ===
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return '🔄 Bot attivo (GET)', 200

@app.route('/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Unsupported content type', 403

if __name__ == "__main__":
    print("🤖 Flask in ascolto...")
    app.run(host="0.0.0.0", port=10000)
