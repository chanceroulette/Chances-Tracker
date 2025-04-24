# ✅ logic/game.py

def initialize_boxes(user_id, chances):
    from logic.state import user_boxes
    user_boxes[user_id] = {chance: [[1], [1], [1], [1]] for chance in chances}

def get_next_bet(user_id):
    from logic.state import user_boxes
    boxes = user_boxes.get(user_id, {})
    bets = {}

    for chance, box_list in boxes.items():
        if len(box_list) >= 2:
            bet = box_list[0][0] + box_list[-1][0]
        elif len(box_list) == 1:
            bet = box_list[0][0]
        else:
            box_list[:] = [[1], [1], [1], [1]]
            bet = 2
        bets[chance] = bet

    return bets

def update_boxes(user_id, winning_chances):
    from logic.state import user_boxes
    boxes = user_boxes.get(user_id, {})

    for chance, box_list in boxes.items():
        if chance in winning_chances:
            if len(box_list) > 1:
                box_list.pop(0)
                box_list.pop(-1)
            elif len(box_list) == 1:
                box_list.pop(0)
        else:
            if len(box_list) >= 2:
                new_val = box_list[0][0] + box_list[-1][0]
            else:
                new_val = box_list[0][0] if box_list else 1
            box_list.append([new_val])

        if len(box_list) == 0:
            box_list[:] = [[1], [1], [1], [1]]
