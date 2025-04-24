# ✅ Contenuto completo e corretto del file logic/state.py

# Dati temporanei per ogni utente
user_numbers = {}           # Numeri inseriti nella fase di analisi
suggested_chances = {}      # Le chances suggerite dopo l’analisi
selected_chances = {}       # Le chances selezionate dall’utente
user_boxes = {}             # Box di gioco per ogni chance selezionata
backup_data = {}            # Backup per funzione Annulla
user_id_phase = {}          # Fase corrente dell'utente

# Costanti per le fasi
PHASE_ANALYSIS = "analysis"       # Inserimento numeri per analisi
PHASE_SELECTION = "selection"     # Selezione chances
PHASE_PLAY = "play"               # Fase di gioco attiva
