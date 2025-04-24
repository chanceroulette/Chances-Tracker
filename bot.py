import telebot
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# ⬇️ Import handler principali
from handlers.analysis import insert_handler, analyze_handler
from handlers.chances import selector
from handlers.core import start_handler, menu_handler
from handlers.play import play_handler
from handlers.undo import undo_handler
from handlers.report import report_handler
from handlers.reset import reset_handler

# ⬇️ Comandi principali
@bot.message_handler(commands=["start"])
def handle_start(message):
    start_handler.handle_start(bot, message)

@bot.message_handler(commands=["menu"])
def handle_menu(message):
    menu_handler.handle_menu(bot, message)

@bot.message_handler(commands=["analizza"])
def handle_analizza(message):
    analyze_handler.handle_analysis(bot, message)

@bot.message_handler(commands=["report"])
def handle_report(message):
    report_handler.handle_report(bot, message)

@bot.message_handler(commands=["reset"])
def handle_reset(message):
    reset_handler.handle_reset(bot, message)

@bot.message_handler(func=lambda msg: msg.text.isdigit())
def handle_number_input(message):
    insert_handler.handle_number_input(bot, message)

# ⬇️ Inline / callback handler
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    play_handler.handle_callback(bot, call)

# ⬇️ Undo da tastiera
@bot.message_handler(func=lambda msg: msg.text == "↩️ Annulla")
def handle_undo(message):
    undo_handler.handle_undo(bot, message)

# ⬇️ Avvio del gioco
@bot.message_handler(func=lambda msg: msg.text == "🎲 Gioca")
def handle_play(message):
    play_handler.handle_play(bot, message)

# ⬇️ Menu
@bot.message_handler(func=lambda msg: msg.text == "☰ Menu")
def handle_menu_btn(message):
    menu_handler.handle_menu(bot, message)

# ⬇️ Conferma finale delle chances selezionate
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_chances"))
def handle_confirm_chances(call):
    play_handler.handle_confirm_chances(bot, call)

# ⬇️ Toggle delle chances selezionabili
@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_"))
def handle_toggle_chance(call):
    play_handler.handle_toggle_chance(bot, call)

# ⬇️ Registrazioni opzionali
selector.register(bot)  # ← questa ora non dà più errore

# ⬇️ Avvia polling o Webhook (Render usa Webhook di solito)
if __name__ == "__main__":
    bot.infinity_polling()
