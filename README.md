# Agenda Turni — Fede

Agenda digitale per la gestione e visualizzazione dei turni mensili.

## Funzionalità

- **Importazione PDF diretta nel browser** — nessun server necessario
- **Visualizzazione multi-mese** con separatori colorati
- **Riunione d'équipe** rilevata automaticamente dal PDF o impostabile manualmente
- **Modifica turni in-line**: operatori, orari e riunione con salvataggio su Firebase
- **Filtro per operatore** con riepilogo ore mensili
- **Grafico Gantt** verticale aggiornato in tempo reale
- **Firebase Firestore** come database — dati visibili online da qualsiasi dispositivo

## Utilizzo rapido

1. Vai su **https://casual70.github.io/Agenda_Fede/**
2. Clicca **⚙ Impostazioni** → seleziona il PDF del mese
3. Clicca **⚙ Elabora PDF** (il browser legge il PDF senza server)
4. Verifica i dati → clicca **💾 Salva su Firebase**

Per istruzioni dettagliate vedi [`ISTRUZIONI_NUOVI_MESI.txt`](ISTRUZIONI_NUOVI_MESI.txt).

## Struttura del progetto

| File | Descrizione |
|------|-------------|
| `index.html` | App principale (parser PDF.js, Firebase, UI) |
| `parse_turni.py` | Parser PDF lato server (alternativo) |
| `inject_data.py` | Inietta JSON in index.html per dati embedded |
| `server.py` | Server Flask locale (fallback, non obbligatorio) |
| `avvia.bat` | Avvia server locale + apre browser automaticamente |
| `turni_MESE_ANNO.json` | Dati parsati per ogni mese |

## Formato dati Firebase

Collezione `turni` — ogni documento rappresenta un giorno:

```json
{
  "id": 3,
  "dayLabel": "Lunedì 3 Agosto",
  "mese": "agosto_2026",
  "riunione": true,
  "shifts": [
    { "name": "NOTTE 2", "op": "CAR", "time": "0:00 - 9:00" },
    { "name": "MATT 1",  "op": "BAD", "time": "8:30 - 14:00" }
  ]
}
```

## Note tecniche

- **Parser browser**: usa PDF.js 3.11 — rileva colonne dinamicamente dall'intestazione del PDF
- **Parser Python**: `parse_turni.py` — usa pdfplumber, stessa logica di rilevamento colonne
- **Multi-mese**: ogni documento ha il campo `mese` (es. `"agosto_2026"`) per separare i mesi
- **Python locale**: usare `python` (PATH → laragon 3.10) per Flask/pdfplumber
