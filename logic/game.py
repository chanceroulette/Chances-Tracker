# logic/game.py

# Ogni utente avrà box separati per ciascuna chance selezionata

def initialize_boxes(chances):
    return {chance: [[1], [1], [1], [1]] for chance in chances}

def get_next_bet(boxes_dict):
    bets = {}
    for chance, boxes in boxes_dict.items():
        bets[chance] = []
        for box in boxes:
            if len(box) == 1:
                bets[chance].append(box[0])
            else:
                bets[chance].append(box[0] + box[-1])
    return bets

def update_boxes(boxes_dict, outcomes):
    # outcomes = dict {chance: win/loss -> True/False}
    updated = {}
    for chance, boxes in boxes_dict.items():
        win = outcomes.get(chance, False)
        new_boxes = []
        for box in boxes:
            if win:
                if len(box) > 1:
                    new_box = box[1:-1]  # rimuove prima e ultima
                else:
                    new_box = []
            else:
                new_val = box[0] + box[-1] if len(box) > 1 else box[0]
                new_box = box + [new_val]
            if not new_box:
                new_box = [1]
            new_boxes.append(new_box)
        updated[chance] = new_boxes
    return updated
