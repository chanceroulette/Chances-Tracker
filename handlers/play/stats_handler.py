from telebot.types import Message
from logic.state import user_data
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(func=lambda m: m.text == "📊 Statistiche")
    def show_stats(message: Message):
        chat_id = message.chat.id

        if chat_id not in user_data or not user_data[chat_id].get("numbers"):
            bot.send_message(
                chat_id,
                "📉 Nessuna giocata registrata al momento.",
                reply_markup=get_main_keyboard()
            )
            return

        nums = user_data[chat_id]["numbers"]
        totale = len(nums)
        ultima = nums[-1]
        media = sum(nums) / totale if totale > 0 else 0

        bot.send_message(
            chat_id,
            (
                f"📊 *Statistiche attuali:*\n\n"
                f"• Numeri inseriti: `{totale}`\n"
                f"• Ultimo numero: `{ultima}`\n"
                f"• Media numerica: `{media:.2f}`"
            ),
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
