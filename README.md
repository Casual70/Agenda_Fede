# Agenda_Fede
Agendo per Fede, lavoro e altro

## 📋 Descrizione
Applicazione web per caricare file PDF, estrarre automaticamente i dati e salvarli in un database Firebase. I dati estratti possono essere visualizzati direttamente nella pagina web.

## ✨ Funzionalità

- 📤 **Caricamento PDF**: Interfaccia semplice per caricare file PDF
- 🔍 **Estrazione Dati**: Estrazione automatica di:
  - Testo completo dal PDF
  - Metadata (titolo, autore, data di creazione)
  - Email
  - Numeri di telefono
  - Date
  - Codici fiscali
  - URL
  - Statistiche (conteggio parole e caratteri)
- 💾 **Salvataggio Firebase**: Tutti i dati estratti vengono salvati automaticamente in Firebase
- 📊 **Visualizzazione Dati**: Interfaccia per visualizzare i dati salvati nel database
- 🔄 **Aggiornamento Real-time**: Pulsante per ricaricare e visualizzare i dati più recenti

## 🚀 Installazione e Configurazione

### Prerequisiti
- Un browser web moderno (Chrome, Firefox, Safari, Edge)
- Un account Firebase (gratuito)

### Setup Firebase

1. Vai su [Firebase Console](https://console.firebase.google.com/)
2. Crea un nuovo progetto o seleziona uno esistente
3. Abilita il **Realtime Database**:
   - Vai su "Build" > "Realtime Database"
   - Clicca su "Create Database"
   - Scegli una location
   - Inizia in modalità test (per lo sviluppo)
4. Ottieni le credenziali dell'app:
   - Vai su "Project Settings" (icona ingranaggio)
   - Scorri fino a "Your apps"
   - Clicca su "</>" per creare una web app
   - Copia la configurazione Firebase

### Configurazione dell'Applicazione

1. Clona o scarica questo repository
2. Apri il file `firebase-config.js`
3. Sostituisci i valori placeholder con le tue credenziali Firebase:

```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    databaseURL: "https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

4. Salva il file

### Regole Firebase Database (Opzionale)

Per un ambiente di produzione, configura le regole di sicurezza nel Firebase Console:

```json
{
  "rules": {
    "pdfDocuments": {
      ".read": true,
      ".write": true
    }
  }
}
```

**Nota**: Le regole sopra sono per lo sviluppo. Per la produzione, implementa regole di sicurezza appropriate con autenticazione.

## 📖 Utilizzo

1. Apri `index.html` nel tuo browser
2. Clicca su "Scegli file" per selezionare un PDF
3. Clicca su "Carica e Analizza"
4. L'applicazione:
   - Estrarrà i dati dal PDF
   - Li mostrerà nella sezione "Dati Estratti dal PDF"
   - Li salverà automaticamente in Firebase
   - Aggiornerà la lista dei "Dati Salvati nel Database"
5. Usa il pulsante "Aggiorna Dati" per ricaricare i dati dal database

📚 **Per esempi dettagliati e casi d'uso**, consulta [EXAMPLES.md](EXAMPLES.md)

## 🛠️ Tecnologie Utilizzate

- **HTML5**: Struttura della pagina
- **CSS3**: Styling e responsive design
- **JavaScript (Vanilla)**: Logica dell'applicazione
- **PDF.js**: Libreria Mozilla per il parsing dei PDF
- **Firebase Realtime Database**: Database cloud per il salvataggio dei dati

## 📁 Struttura del Progetto

```
Agenda_Fede/
│
├── index.html              # Pagina principale
├── style.css              # Stili CSS
├── app.js                 # Logica applicazione
├── firebase-config.js     # Configurazione Firebase
└── README.md             # Documentazione
```

## 🔒 Sicurezza

⚠️ **IMPORTANTE**: 
- Non committare mai le credenziali Firebase reali nel repository pubblico
- Implementa regole di sicurezza Firebase appropriate per la produzione
- Considera l'aggiunta di autenticazione utente per applicazioni production

## 🌐 Deploy

Puoi deployare questa applicazione su:
- **GitHub Pages**
- **Firebase Hosting**
- **Netlify**
- **Vercel**
- Qualsiasi servizio di hosting statico

### Deploy su Firebase Hosting

```bash
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

## 🐛 Troubleshooting

### Il PDF non viene caricato
- Verifica che il file sia effettivamente un PDF
- Controlla la console del browser per eventuali errori

### I dati non vengono salvati in Firebase
- Verifica che le credenziali Firebase siano corrette
- Controlla che il Realtime Database sia abilitato
- Verifica le regole di sicurezza del database

### I dati non vengono visualizzati
- Controlla la console del browser per errori
- Verifica la connessione a Firebase
- Prova a cliccare su "Aggiorna Dati"

## 📝 Licenza

Questo progetto è open source e disponibile sotto la licenza MIT.

## 👤 Autore

Casual70

## 🤝 Contributi

I contributi sono benvenuti! Sentiti libero di aprire issues o pull requests.
