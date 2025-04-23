# logic/state.py

# Stato globale condiviso tra le fasi

# Numeri inseriti dall’utente durante l’analisi
user_numbers = {}            # Es: { user_id: [12, 25, 7, ...] }

# Dati utente durante la fase di gioco
user_data = {}               # Es: { user_id: { phase, numbers, history, boxes, ... } }

# Chances selezionate (sia analisi che avvio rapido)
selected_chances = {}        # Es: { user_id: ["Rosso", "Pari"] }

# Box attivi del sistema per ogni chance e utente
user_boxes = {}              # Es: { user_id: { "Rosso": [[1], [1], [1], [1]], ... } }

# Backup per il tasto ↩️ Annulla
backup_data = {}             # Es: { user_id: { ... } }
