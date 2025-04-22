# 🎰 Chance Roulette Bot

**Bot Telegram per la gestione automatizzata di un sistema di puntata su roulette europea, basato su chances semplici (Rosso/Nero, Pari/Dispari, Manque/Passe).**

Sviluppato da: **Fabio Felice Cudia**

---

## 🚀 Funzionalità principali

- 🎯 Inserimento numeri tramite tastiera numerica inline (0–36)
- 📊 Analisi statistica delle ultime 15 uscite
- ✅ Selezione personalizzata delle chances attive
- 💼 Gestione intelligente dei box (4 fiches per chance)
- 🔄 Comando *Annulla ultima giocata* con ripristino completo
- ⚡ Avvio rapido senza inserimento numeri
- 🔐 Accesso area admin tramite comando `/admin`

---

## 🧠 Strategia implementata

- Ogni chance ha un proprio *box* con 4 fiches.
- Si gioca la somma della prima + ultima fiche.
- Se si vince: si eliminano prima e ultima.
- Se si perde: si aggiunge in fondo la somma puntata.
- Quando il box si svuota: viene rigenerato da zero.

---
