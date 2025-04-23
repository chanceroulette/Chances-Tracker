# logic/state.py

# FASE 1: ANALISI
user_numbers = {}  # user_id: [numeri inseriti]
suggested_chances = {}  # user_id: [chances suggerite]
selected_chances = {}  # user_id: set(chances selezionate)

# FASE 2: GIOCO
user_boxes = {}  # user_id: {chance: [box]}
user_id_phase = {}  # user_id: "analysis" | "selection" | "game"

# Backup per annullare
backup_data = {}  # user_id: [numeri prima dell'ultima giocata]
