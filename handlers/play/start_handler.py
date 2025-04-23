# handlers/play/start_handler.py
from telebot.types import Message
from messages.keyboard import get_main_keyboard


def register(bot):
    @bot.message_handler(commands=["start"])
    def start(message: Message):
        bot.send_message(
            message.chat.id,
            "🎰 *Benvenuto su ChanceTracker!*

"
            "📌 Questo bot ti aiuta a simulare una strategia alla roulette basata sulle chances semplici (Rosso/Nero, Pari/Dispari, ecc).

"
            "🔍 Puoi iniziare con *Analisi* delle ultime estrazioni o andare direttamente con *Avvio rapido*.

"
            "🎯 Dopo aver scelto le chances, il sistema inizierà a suggerire puntate usando il metodo a *box*.",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
