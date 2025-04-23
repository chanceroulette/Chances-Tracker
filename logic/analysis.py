def analyze_chances(numbers):
    stats = {
        "Rosso": 0, "Nero": 0,
        "Pari": 0, "Dispari": 0,
        "Manque": 0, "Passe": 0
    }

    red_numbers = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    for num in numbers:
        if num in red_numbers:
            stats["Rosso"] += 1
        else:
            stats["Nero"] += 1

        if num != 0:
            stats["Pari" if num % 2 == 0 else "Dispari"] += 1
            stats["Manque" if num <= 18 else "Passe"] += 1

    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    top_chances = [chance for chance, _ in sorted_stats[:3]]
    return top_chances
