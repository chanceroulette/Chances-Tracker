# selector.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.analysis import analyze_chances
from logic.state import selected_chances

# Funzione per creare markup della tastiera delle chances
def build_chances_keyboard(chat_id, suggerite):
    markup = InlineKeyboardMarkup(row_width=2)
    for chance in ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]:
        prefix = "✅ " if chance in selected_chances.get(chat_id, []) else "⬜️ "
        markup.add(InlineKeyboardButton(f"{prefix}{chance}", callback_data=f"toggle_{chance}"))
    markup.add(InlineKeyboardButton("🎯 Conferma e inizia il gioco", callback_data="conferma_chances"))
    return markup

def show_chances_selection(bot, chat_id, numbers):
    suggerite = analyze_chances(numbers) if numbers else []
    selected_chances[chat_id] = suggerite.copy()
    text = (
        f"🔍 *Suggerite:* {', '.join(suggerite) if suggerite else 'nessuna'}\n"
        f"Scegli le chances che vuoi usare:"
    )
    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=build_chances_keyboard(chat_id, suggerite))
