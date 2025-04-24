from telebot.types import Message
from logic.state import user_numbers
from logic.analysis import get_top_chances
from handlers.chances.selector import show_chances_selection

def handle_analysis(bot, message: Message):
    user_id = message.from_user.id
    numbers = user_numbers.get(user_id, [])

    if len(numbers) < 10:
        bot.send_message(
            message.chat.id,
            f"⚠️ Hai inserito solo {len(numbers)} numeri.\nInseriscine almeno 10 per poter effettuare l'analisi."
        )
        return

    # Analizza le chances più frequenti tra i numeri inseriti
    top_chances = get_top_chances(numbers, limit=3)

    # Passa alla fase di selezione con le chances suggerite
    show_chances_selection(bot, message, top_chances)
