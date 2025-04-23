# messages/play.py

def get_start_message(chances):
    formatted = ", ".join([f"*{c}*" for c in chances])
    return (
        f"🎯 *Inizio del Gioco!*\n\n"
        f"Chances attive: {formatted}\n\n"
        "Inserisci il *numero uscito* nella roulette tramite la tastiera.\n"
        "Il sistema ti dirà cosa puntare al prossimo turno. Buona fortuna!"
    )
