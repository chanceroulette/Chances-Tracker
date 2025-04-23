# handlers/play/stats_handler.py
from telebot.types import Message
from logic.state import user_data
from messages.keyboard import get_main_keyboard


def register(bot):
    @bot.message_handler(func=lambda m: m.text == "📊 Statistiche")
    def show_stats(message: Message):
        chat_id = message.chat.id
        data = user_data.get(chat_id, {})
        numbers = data.get("numbers", [])

        if not numbers:
            bot.send_message(
                chat_id,
                "📉 Nessuna giocata registrata per ora.",
                reply_markup=get_main_keyboard()
            )
            return

        totale = len(numbers)
        ultima = numbers[-1]
        media = sum(numbers) / totale

        bot.send_message(
            chat_id,
            f"📊 *Statistiche attuali:*
\n• Numeri inseriti: {totale}
• Ultimo numero: `{ultima}`
• Media: `{media:.2f}`",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
