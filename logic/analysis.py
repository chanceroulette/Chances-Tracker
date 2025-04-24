from collections import Counter

# Mappature fisse per le chances semplici
RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
BLACK_NUMBERS = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

def classify_chances(number):
    """Restituisce una lista di chances a cui il numero appartiene"""
    chances = []
    if number in RED_NUMBERS:
        chances.append("Rosso")
    elif number in BLACK_NUMBERS:
        chances.append("Nero")

    if number != 0:
        if number % 2 == 0:
            chances.append("Pari")
        else:
            chances.append("Dispari")

        if 1 <= number <= 18:
            chances.append("Manque")
        elif 19 <= number <= 36:
            chances.append("Passe")
    return chances

def get_top_chances(numbers, limit=3):
    """Analizza i numeri e restituisce le 'limit' chances più frequenti"""
    all_chances = []
    for number in numbers:
        all_chances.extend(classify_chances(number))

    counter = Counter(all_chances)
    top = counter.most_common(limit)
    return [chance for chance, _ in top]
