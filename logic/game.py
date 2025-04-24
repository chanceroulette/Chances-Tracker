from collections import defaultdict
from logic.state import user_boxes

# Inizializza 4 box da 1 fiche per ciascuna chance selezionata
def initialize_boxes(user_id, chances):
    user_boxes[user_id] = {}
    for chance in chances:
        user_boxes[user_id][chance] = [1, 1, 1, 1]

# Calcola la prossima puntata per ogni chance attiva
def get_next_bet(user_id):
    bets = {}
    for chance, box in user_boxes[user_id].items():
        if len(box) == 1:
            bets[chance] = box[0]
        else:
            bets[chance] = box[0] + box[-1]
    return bets

# Aggiorna i box in base al numero uscito (mock logica vincente)
def update_boxes(user_id, numero):
    for chance, box in user_boxes[user_id].items():
        win = is_win(chance, numero)
        if win:
            # Rimuove la prima e l’ultima fiche se ci sono almeno 2 elementi
            if len(box) > 1:
                box.pop(0)
                box.pop(-1)
        else:
            # Aggiunge in fondo la somma delle due fiche giocate
            if len(box) == 1:
                new_bet = box[0]
            else:
                new_bet = box[0] + box[-1]
            box.append(new_bet)

        # Se il box si svuota, lo ricrea da 4 fiche da 1
        if len(box) == 0:
            user_boxes[user_id][chance] = [1, 1, 1, 1]

# Mock: logica per decidere se la chance ha vinto o perso
def is_win(chance, numero):
    if chance == "Rosso":
        return numero in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
    elif chance == "Nero":
        return numero in [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
    elif chance == "Pari":
        return numero != 0 and numero % 2 == 0
    elif chance == "Dispari":
        return numero % 2 == 1
    elif chance == "Manque":
        return 1 <= numero <= 18
    elif chance == "Passe":
        return 19 <= numero <= 36
    return False
