# logic/game.py

# Simulazione della logica "box" per ciascuna chance selezionata

# Ogni box è una lista di numeri che rappresentano fiches
def initialize_boxes():
    return [[1], [1], [1], [1]]  # 4 box da 1 fiche

def get_next_bet(boxes):
    # Calcola la prossima puntata: somma prima + ultima fiche di ogni box
    bets = []
    for box in boxes:
        if len(box) == 1:
            bets.append(box[0])
        else:
            bets.append(box[0] + box[-1])
    return bets

def update_boxes(boxes, results, win_flags):
    new_boxes = []
    for i, win in enumerate(win_flags):
        box = boxes[i]
        if win:
            if len(box) > 1:
                new_boxes.append(box[1:-1])  # rimuove prima e ultima
            else:
                new_boxes.append([])  # svuota
        else:
            new_value = box[0] + box[-1] if len(box) > 1 else box[0]
            new_boxes.append(box + [new_value])
    # Ricrea box vuoti con [1]
    return [b if b else [1] for b in new_boxes]
