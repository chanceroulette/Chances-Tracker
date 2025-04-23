from handlers.play_handler import user_data
from telebot.types import Message
from messages.keyboard import get_main_keyboard

def register(bot):
    @bot.message_handler(func=lambda message: message.text == "📊 Statistiche")
    def stats(message: Message):
        user_id = message.from_user.id

        if user_id not in user_data or len(user_data[user_id]) == 0:
            bot.send_message(
                message.chat.id,
                "📉 Nessuna giocata registrata per ora.",
                reply_markup=get_main_keyboard()
            )
            return

        nums = user_data[user_id]
        totale = len(nums)
        ultima = nums[-1]
        media = sum(nums) / totale if totale > 0 else 0

        bot.send_message(
            message.chat.id,
            f"📊 *Statistiche attuali*\n\n"
            f"• Numeri inseriti: {totale}\n"
            f"• Ultimo numero: `{ultima}`\n"
            f"• Media numerica: `{media:.2f}`",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
