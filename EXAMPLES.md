# Esempi d'Uso - Agenda Fede

## 📝 Guida Rapida

Questo documento fornisce esempi pratici di come utilizzare l'applicazione Agenda Fede per l'estrazione di dati dai PDF.

## 🎯 Tipi di Dati Estratti

L'applicazione è in grado di estrarre automaticamente i seguenti tipi di dati dai file PDF:

### 1. **Testo Completo**
- Tutto il testo contenuto nel PDF viene estratto e salvato
- Utile per ricerche full-text e analisi del contenuto

### 2. **Metadata del PDF**
- Titolo del documento
- Autore
- Oggetto/Subject
- Creatore (software usato per creare il PDF)
- Producer (software usato per generare il PDF)
- Data di creazione

### 3. **Informazioni di Contatto**
- **Email**: Tutte le email presenti nel documento
  - Esempio: `info@example.com`, `utente@dominio.it`
- **Numeri di Telefono**: Numeri italiani e internazionali
  - Formato italiano: `+39 123 456 7890`, `0123456789`, `3401234567`
  - Formati riconosciuti: con o senza prefisso internazionale

### 4. **Date**
- Date in vari formati
  - Esempio: `01/12/2024`, `2024-12-01`, `01.12.2024`

### 5. **Codici Fiscali**
- Codici fiscali italiani nel formato standard
  - Esempio: `RSSMRA80A01H501U`

### 6. **URL**
- Indirizzi web presenti nel documento
  - Esempio: `https://www.example.com`, `http://sito.it`

### 7. **Statistiche**
- Conteggio parole
- Conteggio caratteri
- Numero di pagine

## 💡 Casi d'Uso Comuni

### 📄 Fatture e Documenti Commerciali
- Estrai dati di contatto di fornitori e clienti
- Identifica date di emissione e scadenza
- Archivia automaticamente nel database

### 📋 CV e Curricula
- Estrai email e numeri di telefono dei candidati
- Identifica URL di portfolio o profili LinkedIn
- Mantieni un database centralizzato di candidature

### 📑 Contratti e Documenti Legali
- Estrai date importanti (firme, scadenze)
- Identifica parti coinvolte tramite codici fiscali
- Archivia documenti per riferimenti futuri

### 📧 Corrispondenza
- Estrai tutti i contatti dalle comunicazioni
- Identifica date di invio e ricevimento
- Mantieni uno storico ricercabile

## 🔍 Esempio Pratico

### Input: PDF con i seguenti contenuti
```
Fattura N. 2024/001
Data: 15/01/2024

Cliente: Mario Rossi
Codice Fiscale: RSSMRA80A01H501U
Email: mario.rossi@email.it
Telefono: +39 340 1234567

Dettagli fattura...
```

### Output Estratto
```json
{
  "fileName": "fattura_2024_001.pdf",
  "numPages": 1,
  "metadata": {
    "title": "Fattura 2024/001",
    "author": "Azienda S.r.l."
  },
  "structuredData": {
    "emails": ["mario.rossi@email.it"],
    "phones": ["+39 340 1234567"],
    "dates": ["15/01/2024"],
    "codiciFiscali": ["RSSMRA80A01H501U"],
    "wordCount": 150,
    "charCount": 856
  },
  "extractedText": "Fattura N. 2024/001 Data: 15/01/2024 ..."
}
```

## 🔄 Workflow Tipico

1. **Carica PDF**
   - Clicca su "Choose File" e seleziona il PDF
   - Clicca su "Carica e Analizza"

2. **Visualizza Dati Estratti**
   - I dati vengono mostrati immediatamente nella sezione "Dati Estratti dal PDF"
   - Verifica che tutti i dati importanti siano stati identificati

3. **Salvataggio Automatico**
   - I dati vengono salvati automaticamente in Firebase
   - Non è necessaria nessuna azione aggiuntiva

4. **Consulta Dati Salvati**
   - Clicca su "Aggiorna Dati" per vedere gli ultimi documenti salvati
   - Scorri la lista per trovare documenti precedenti

## 🎨 Caratteristiche dell'Interfaccia

### Feedback Visivo
- **Verde**: Operazione completata con successo
- **Blu**: Operazione in corso
- **Rosso**: Errore o problema

### Sezioni Interattive
- **Carica PDF**: Upload e analisi del documento
- **Dati Estratti dal PDF**: Visualizzazione dei dati appena estratti
- **Dati Salvati nel Database**: Storico dei documenti elaborati

## ⚡ Suggerimenti per l'Uso

1. **Qualità del PDF**: 
   - PDF generati digitalmente funzionano meglio
   - PDF scansionati potrebbero richiedere OCR (non incluso in questa versione)

2. **Dimensione File**:
   - L'applicazione gestisce PDF di varie dimensioni
   - Per file molto grandi (>10MB), il processo potrebbe richiedere più tempo

3. **Privacy dei Dati**:
   - Configura correttamente le regole Firebase per proteggere i dati sensibili
   - Non caricare documenti confidenziali su Firebase pubblico

4. **Formato Date**:
   - L'app riconosce formati comuni: DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY

5. **Numeri di Telefono**:
   - Ottimizzato per numeri italiani
   - Supporta formati con e senza prefisso internazionale

## 🔧 Personalizzazione

Puoi modificare i pattern di ricerca in `app.js` nella funzione `extractStructuredData()` per adattarli alle tue esigenze specifiche:

- Modifica le regex per riconoscere altri formati
- Aggiungi nuovi tipi di dati da estrarre
- Personalizza la visualizzazione dei risultati

## 📊 Gestione dei Dati

### Firebase Database
I dati sono organizzati così:
```
pdfDocuments/
  ├─ -MXyZ123abc...
  │   ├─ fileName: "documento.pdf"
  │   ├─ extractedText: "..."
  │   ├─ metadata: {...}
  │   └─ structuredData: {...}
  └─ -MXyZ456def...
      └─ ...
```

### Limite di Visualizzazione
- Di default vengono mostrati gli ultimi 10 documenti caricati
- Puoi modificare questo limite nel codice (variabile `limitToLast(10)`)

## ❓ Domande Frequenti

**Q: Il PDF non viene analizzato correttamente**
A: Assicurati che il file sia un vero PDF e non un'immagine rinominata

**Q: Alcuni dati non vengono estratti**
A: Le regex potrebbero non coprire tutti i formati. Personalizzale in base alle tue esigenze

**Q: Posso cercare nei documenti salvati?**
A: Questa versione base non include ricerca. Puoi estendere l'app con funzionalità di ricerca Firebase

**Q: Come elimino documenti vecchi?**
A: Usa la console Firebase per gestire i documenti nel database

## 🚀 Prossimi Sviluppi Possibili

- Ricerca full-text nei documenti
- Esportazione dati in CSV/Excel
- OCR per PDF scansionati
- Autenticazione utenti
- Organizzazione per categorie/tag
- Dashboard con statistiche

---

Per supporto o domande, consulta il README.md principale o apri una issue su GitHub.
