def register(bot):
    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(message.chat.id, "ℹ️ Questo bot ti aiuta a simulare un sistema sulla roulette europea.")