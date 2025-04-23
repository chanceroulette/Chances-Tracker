import os
import telebot
from flask import Flask, request
from dotenv import load_dotenv

from messages.welcome import get_welcome_message
from messages.keyboard import get_main_keyboard
from handlers import (
    start_handler,
    analyze_handler,
    play_box_handler,
    play_handler,
    chances_selector,  # importa solo, ma non registrare
    undo_handler,
    stats_handler,
    reset_handler,
    help_handler,
    menu_handler
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Webhook Flask
@app.route("/", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "", 200

@app.route("/", methods=["GET"])
def index():
    return "✅ Bot attivo su Flask!", 200

# Comando /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        get_welcome_message(),
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

# Registrazione handler
start_handler.register(bot)
analyze_handler.register(bot)
play_box_handler.register(bot)
play_handler.register(bot)
undo_handler.register(bot)
stats_handler.register(bot)
reset_handler.register(bot)
help_handler.register(bot)
menu_handler.register(bot)
# chances_selector.register(bot)  <-- RIMOSSO perché non esiste

# Avvio bot
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print("🔁 Webhook aggiornato all’avvio")
    print("🚀 Avvio Flask...")
    app.run(host="0.0.0.0", port=10000)
