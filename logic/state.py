# logic/state.py

# Numeri inseriti dall’utente per l’analisi
user_data = {}

# Copia dei dati per l’annullamento
backup_data = {}

# Chances attive selezionate (via analisi o avvio rapido)
active_chances = {}

def get_user_data():
    return user_data

def get_backup_data():
    return backup_data

def get_active_chances():
    return active_chances
