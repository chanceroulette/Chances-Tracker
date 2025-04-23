from logic.state import user_boxes

# Inizializza 4 box con 1 fiche per ogni chance selezionata
def initialize_boxes(user_id, chances):
    user_boxes[user_id] = {}
    for chance in chances:
        user_boxes[user_id][chance] = [[1], [1], [1], [1]]

# Calcola le prossime puntate in base ai box attuali
def get_next_bet(chances_boxes):
    bets = {}
    for chance, boxes in chances_boxes.items():
        if len(boxes) == 1:
            bets[chance] = boxes[0][0]
        else:
            bets[chance] = boxes[0][0] + boxes[-1][0]
    return bets

# Aggiorna i box dopo un numero uscito, simulando vincite/perdite
def update_boxes(user_id, numero):
    from logic.utils import evaluate_chance  # funzione ausiliaria per calcolare vincite

    chances_boxes = user_boxes[user_id]
    dettagli = {}
    totale_vinti = 0
    totale_persi = 0

    for chance, boxes in chances_boxes.items():
        if len(boxes) == 0:
            boxes.extend([[1], [1], [1], [1]])

        puntata = boxes[0][0] if len(boxes) == 1 else boxes[0][0] + boxes[-1][0]
        risultato = evaluate_chance(chance, numero)

        if risultato:  # Vinto
            totale_vinti += puntata
            if len(boxes) > 1:
                boxes.pop()  # rimuove ultimo
                boxes.pop(0)  # rimuove primo
            else:
                boxes.pop()
        else:  # Perso
            totale_persi += puntata
            boxes.append([puntata])

        if len(boxes) == 0:
            boxes.extend([[1], [1], [1], [1]])

        dettagli[chance] = "vinto" if risultato else "perso"

    return {
        "dettagli": dettagli,
        "vinti": totale_vinti,
        "persi": totale_persi,
        "delta": totale_vinti - totale_persi
    }
