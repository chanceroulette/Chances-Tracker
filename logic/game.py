# logic/game.py
from logic.state import user_boxes


def initialize_boxes(chat_id, chances):
    user_boxes[chat_id] = {ch: [[1], [1], [1], [1]] for ch in chances}


def get_next_bets(chat_id):
    if chat_id not in user_boxes:
        return {}
    next_bets = {}
    for chance, boxes in user_boxes[chat_id].items():
        if len(boxes) == 1:
            next_bets[chance] = sum(boxes[0])
        else:
            next_bets[chance] = boxes[0][0] + boxes[-1][0]
    return next_bets


def update_boxes(chat_id, winning_chances):
    if chat_id not in user_boxes:
        return

    for chance, boxes in user_boxes[chat_id].items():
        if chance in winning_chances:
            if len(boxes) > 1:
                boxes.pop(0)
                boxes.pop(-1)
            elif len(boxes) == 1:
                boxes.pop()
        else:
            if len(boxes) >= 2:
                new_val = boxes[0][0] + boxes[-1][0]
            elif boxes:
                new_val = boxes[0][0]
            else:
                new_val = 1
            boxes.append([new_val])

        if not boxes:
            boxes.extend([[1], [1], [1], [1]])
