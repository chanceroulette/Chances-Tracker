# handlers/chances/selector.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic.state import suggested_chances, selected_chances

ALL_CHANCES = ["Rosso", "Nero", "Pari", "Dispari", "Manque", "Passe"]

def show_chances_selection(bot, chat_id, numbers):
    freq = {"Rosso": 0, "Nero": 0, "Pari": 0, "Dispari": 0, "Manque": 0, "Passe": 0}
    for n in numbers:
        if n == 0: continue
        if n % 2 == 0:
            freq["Pari"] += 1
        else:
            freq["Dispari"] += 1
        if 1 <= n <= 18:
            freq["Manque"] += 1
        else:
            freq["Passe"] += 1
        if n in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]:
            freq["Rosso"] += 1
        else:
            freq["Nero"] += 1

    sorted_chances = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    best = [ch[0] for ch in sorted_chances[:3]]
    suggested_chances[chat_id] = best
    selected_chances[chat_id] = set(best)

    msg = f"\U0001F50D *Suggerite:* {', '.join(best)}\n\nSeleziona le chances da attivare:"
    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=get_chance_markup(chat_id))

def get_chance_markup(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for ch in ALL_CHANCES:
        prefix = "✅ " if ch in selected_chances[chat_id] else "☐ "
        buttons.append(InlineKeyboardButton(prefix + ch, callback_data=f"toggle_{ch}"))
    markup.add(*buttons)
    markup.add(InlineKeyboardButton("✔️ Conferma", callback_data="confirm_chances"))
    return markup
