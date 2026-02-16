// Firebase Configuration
// IMPORTANTE: Sostituire con le proprie credenziali Firebase
// Per ottenere le credenziali:
// 1. Vai su https://console.firebase.google.com/
// 2. Crea un nuovo progetto o seleziona uno esistente
// 3. Vai su Impostazioni progetto > Le tue app
// 4. Copia la configurazione dell'app web

const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    databaseURL: "https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// Inizializza Firebase
try {
    firebase.initializeApp(firebaseConfig);
    console.log('Firebase inizializzato con successo');
} catch (error) {
    console.error('Errore durante l\'inizializzazione di Firebase:', error);
}

// Riferimento al database
const database = firebase.database();
