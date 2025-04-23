# bot.py
import os
import telebot
from flask import Flask, request
from dotenv import load_dotenv

# Carica variabili d’ambiente
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Importa handler da tutte le fasi (analisi, selezione, gioco)
from handlers.analysis import insert_handler, analyze_handler
from handlers.chances import selector, callbacks
from handlers.play import (
    start_handler,
    help_handler,
    menu_handler,
    play_handler,
    play_box_handler,
    reset_handler,
    stats_handler,
    undo_handler
)

# Registra tutti i moduli
insert_handler.register(bot)
analyze_handler.register(bot)
selector.register(bot)
callbacks.register(bot)

start_handler.register(bot)
help_handler.register(bot)
menu_handler.register(bot)
play_handler.register(bot)
play_box_handler.register(bot)
reset_handler.register(bot)
stats_handler.register(bot)
undo_handler.register(bot)

# Webhook
@bot.message_handler(commands=["webhook"])
def webhook(message):
    bot.set_webhook(url=WEBHOOK_URL)
    bot.send_message(message.chat.id, "🔗 Webhook impostato!")

@app.route("/", methods=["POST"])
def webhook_handler():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "", 200
    return "Hello from Flask!", 200

# Avvia Flask
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print("🔁 Webhook aggiornato all’avvio")
    print("🚀 Avvio Flask...")
    app.run(host="0.0.0.0", port=10000)
