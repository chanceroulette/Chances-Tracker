from telebot.types import Message
from logic.state import suggested_chances, selected_chances, user_id_phase, PHASE_SELECTION
from messages.keyboard import get_main_keyboard
from messages.chances_keyboard import get_chances_keyboard

def show_chances_selection(bot, message: Message, user_id: int):
    user_id_phase[user_id] = PHASE_SELECTION
    selected_chances[user_id] = []

    suggerite = suggested_chances.get(user_id, [])
    suggerite_text = f"🔍 *Suggerite:* {', '.join(suggerite)}\n\n" if suggerite else ""

    bot.send_message(
        message.chat.id,
        f"{suggerite_text}"
        "☑️ Seleziona da *1 a 6* chances semplici per iniziare a giocare.\n"
        "_Quando hai finito, premi Conferma._",
        parse_mode='Markdown',
        reply_markup=get_chances_keyboard(user_id)
    )

# ✅ Aggiunta per evitare l'errore nel bot.py
def register(bot):
    # Non serve registrare nulla qui, ma la funzione deve esistere
    pass
