from telebot.types import Message

def register_test(bot):
    @bot.message_handler(func=lambda message: True)
    def handle_test(message: Message):
        print(f"📩 Messaggio ricevuto: {message.text} da {message.chat.id}")
        bot.send_message(message.chat.id, "✅ Ricevuto!")
