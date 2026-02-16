// Configurazione PDF.js
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

// Elementi DOM
const pdfInput = document.getElementById('pdfInput');
const uploadBtn = document.getElementById('uploadBtn');
const refreshBtn = document.getElementById('refreshBtn');
const uploadStatus = document.getElementById('uploadStatus');
const extractedDataDiv = document.getElementById('extractedData');
const savedDataDiv = document.getElementById('savedData');

// Stato dell'applicazione
let currentPdfData = null;

// Event Listeners
uploadBtn.addEventListener('click', handleUpload);
refreshBtn.addEventListener('click', loadSavedData);

// Carica i dati salvati all'avvio
document.addEventListener('DOMContentLoaded', () => {
    loadSavedData();
});

/**
 * Gestisce il caricamento e l'analisi del PDF
 */
async function handleUpload() {
    const file = pdfInput.files[0];
    
    if (!file) {
        showStatus('Seleziona un file PDF', 'error');
        return;
    }
    
    if (file.type !== 'application/pdf') {
        showStatus('Il file selezionato non è un PDF', 'error');
        return;
    }
    
    uploadBtn.disabled = true;
    showStatus('Caricamento e analisi del PDF in corso...', 'info');
    
    try {
        // Leggi il file come ArrayBuffer
        const arrayBuffer = await file.arrayBuffer();
        
        // Estrai i dati dal PDF
        const extractedData = await extractPdfData(arrayBuffer, file.name);
        
        // Mostra i dati estratti
        displayExtractedData(extractedData);
        
        // Salva nel database Firebase
        await saveToFirebase(extractedData);
        
        showStatus('PDF analizzato e dati salvati con successo!', 'success');
        
        // Ricarica i dati salvati
        await loadSavedData();
        
        // Reset input
        pdfInput.value = '';
        
    } catch (error) {
        console.error('Errore:', error);
        showStatus(`Errore: ${error.message}`, 'error');
    } finally {
        uploadBtn.disabled = false;
    }
}

/**
 * Estrae i dati dal PDF
 */
async function extractPdfData(arrayBuffer, fileName) {
    try {
        const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
        const numPages = pdf.numPages;
        let fullText = '';
        
        // Estrai il testo da ogni pagina
        for (let i = 1; i <= numPages; i++) {
            const page = await pdf.getPage(i);
            const textContent = await page.getTextContent();
            const pageText = textContent.items.map(item => item.str).join(' ');
            fullText += pageText + '\n';
        }
        
        // Estrai informazioni utili
        const metadata = await pdf.getMetadata();
        
        // Crea oggetto con i dati estratti
        const extractedData = {
            fileName: fileName,
            numPages: numPages,
            extractedText: fullText.trim(),
            metadata: {
                title: metadata.info?.Title || 'N/A',
                author: metadata.info?.Author || 'N/A',
                subject: metadata.info?.Subject || 'N/A',
                creator: metadata.info?.Creator || 'N/A',
                producer: metadata.info?.Producer || 'N/A',
                creationDate: metadata.info?.CreationDate || 'N/A'
            },
            uploadDate: new Date().toISOString(),
            timestamp: Date.now()
        };
        
        // Tenta di estrarre dati strutturati comuni
        extractedData.structuredData = extractStructuredData(fullText);
        
        return extractedData;
        
    } catch (error) {
        throw new Error(`Errore nell'estrazione dei dati dal PDF: ${error.message}`);
    }
}

/**
 * Tenta di estrarre dati strutturati dal testo
 */
function extractStructuredData(text) {
    const structured = {};
    
    // Cerca email
    const emailRegex = /[\w.-]+@[\w.-]+\.\w+/g;
    const emails = text.match(emailRegex);
    if (emails && emails.length > 0) {
        structured.emails = [...new Set(emails)];
    }
    
    // Cerca numeri di telefono (formato italiano e internazionale)
    const phoneRegex = /(\+?\d{1,4}[\s-]?)?\(?\d{1,4}\)?[\s.-]?\d{1,4}[\s.-]?\d{1,9}/g;
    const phones = text.match(phoneRegex);
    if (phones && phones.length > 0) {
        structured.phones = [...new Set(phones.filter(p => p.length >= 8))];
    }
    
    // Cerca date (vari formati)
    const dateRegex = /\b\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}\b/g;
    const dates = text.match(dateRegex);
    if (dates && dates.length > 0) {
        structured.dates = [...new Set(dates)];
    }
    
    // Cerca codici fiscali italiani
    const cfRegex = /\b[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]\b/g;
    const codiciFiscali = text.match(cfRegex);
    if (codiciFiscali && codiciFiscali.length > 0) {
        structured.codiciFiscali = [...new Set(codiciFiscali)];
    }
    
    // Cerca URL
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const urls = text.match(urlRegex);
    if (urls && urls.length > 0) {
        structured.urls = [...new Set(urls)];
    }
    
    // Conta parole e caratteri
    structured.wordCount = text.split(/\s+/).filter(w => w.length > 0).length;
    structured.charCount = text.length;
    
    return structured;
}

/**
 * Mostra i dati estratti nell'interfaccia
 */
function displayExtractedData(data) {
    let html = '<div class="data-item">';
    html += `<h3>📄 ${data.fileName}</h3>`;
    html += `<p><strong>Numero di pagine:</strong> ${data.numPages}</p>`;
    
    // Metadata
    html += '<p><strong>Metadata:</strong></p>';
    html += '<ul style="margin-left: 20px;">';
    html += `<li>Titolo: ${data.metadata.title}</li>`;
    html += `<li>Autore: ${data.metadata.author}</li>`;
    html += `<li>Oggetto: ${data.metadata.subject}</li>`;
    html += '</ul>';
    
    // Dati strutturati
    if (data.structuredData) {
        html += '<p><strong>Dati Estratti:</strong></p>';
        html += '<ul style="margin-left: 20px;">';
        
        if (data.structuredData.emails) {
            html += `<li>Email trovate: ${data.structuredData.emails.join(', ')}</li>`;
        }
        if (data.structuredData.phones) {
            html += `<li>Telefoni trovati: ${data.structuredData.phones.join(', ')}</li>`;
        }
        if (data.structuredData.dates) {
            html += `<li>Date trovate: ${data.structuredData.dates.join(', ')}</li>`;
        }
        if (data.structuredData.codiciFiscali) {
            html += `<li>Codici Fiscali: ${data.structuredData.codiciFiscali.join(', ')}</li>`;
        }
        if (data.structuredData.urls) {
            html += `<li>URL trovati: ${data.structuredData.urls.slice(0, 3).join(', ')}${data.structuredData.urls.length > 3 ? '...' : ''}</li>`;
        }
        
        html += `<li>Parole: ${data.structuredData.wordCount}</li>`;
        html += `<li>Caratteri: ${data.structuredData.charCount}</li>`;
        html += '</ul>';
    }
    
    // Testo estratto (primi 500 caratteri)
    const previewText = data.extractedText.substring(0, 500);
    html += '<p><strong>Anteprima testo estratto:</strong></p>';
    html += `<div class="extracted-content">${previewText}${data.extractedText.length > 500 ? '...' : ''}</div>`;
    
    html += `<p class="timestamp">Caricato: ${new Date(data.uploadDate).toLocaleString('it-IT')}</p>`;
    html += '</div>';
    
    extractedDataDiv.innerHTML = html;
    currentPdfData = data;
}

/**
 * Salva i dati nel database Firebase
 */
async function saveToFirebase(data) {
    try {
        const ref = database.ref('pdfDocuments');
        const newDocRef = ref.push();
        await newDocRef.set(data);
        console.log('Dati salvati in Firebase con ID:', newDocRef.key);
        return newDocRef.key;
    } catch (error) {
        throw new Error(`Errore nel salvataggio su Firebase: ${error.message}`);
    }
}

/**
 * Carica i dati salvati dal database Firebase
 */
async function loadSavedData() {
    refreshBtn.disabled = true;
    
    try {
        const ref = database.ref('pdfDocuments');
        const snapshot = await ref.orderByChild('timestamp').limitToLast(10).once('value');
        
        if (!snapshot.exists()) {
            savedDataDiv.innerHTML = '<p class="empty-state">Nessun dato salvato nel database.</p>';
            return;
        }
        
        // Converti i dati in array e ordina per timestamp decrescente
        const dataArray = [];
        snapshot.forEach((childSnapshot) => {
            dataArray.push({
                id: childSnapshot.key,
                ...childSnapshot.val()
            });
        });
        
        dataArray.sort((a, b) => b.timestamp - a.timestamp);
        
        // Mostra i dati
        let html = '';
        dataArray.forEach((doc) => {
            html += '<div class="data-item">';
            html += `<h3>📄 ${doc.fileName}</h3>`;
            html += `<p><strong>Pagine:</strong> ${doc.numPages}</p>`;
            
            if (doc.metadata) {
                html += `<p><strong>Titolo:</strong> ${doc.metadata.title}</p>`;
                html += `<p><strong>Autore:</strong> ${doc.metadata.author}</p>`;
            }
            
            if (doc.structuredData) {
                if (doc.structuredData.emails && doc.structuredData.emails.length > 0) {
                    html += `<p><strong>Email:</strong> ${doc.structuredData.emails.join(', ')}</p>`;
                }
                if (doc.structuredData.phones && doc.structuredData.phones.length > 0) {
                    html += `<p><strong>Telefoni:</strong> ${doc.structuredData.phones.join(', ')}</p>`;
                }
                if (doc.structuredData.wordCount) {
                    html += `<p><strong>Parole:</strong> ${doc.structuredData.wordCount}</p>`;
                }
            }
            
            const previewText = doc.extractedText ? doc.extractedText.substring(0, 200) : '';
            if (previewText) {
                html += '<p><strong>Anteprima:</strong></p>';
                html += `<div class="extracted-content">${previewText}...</div>`;
            }
            
            html += `<p class="timestamp">Salvato: ${new Date(doc.uploadDate).toLocaleString('it-IT')}</p>`;
            html += '</div>';
        });
        
        savedDataDiv.innerHTML = html;
        
    } catch (error) {
        console.error('Errore nel caricamento dei dati:', error);
        savedDataDiv.innerHTML = `<p class="empty-state" style="color: #dc3545;">Errore nel caricamento dei dati: ${error.message}</p>`;
    } finally {
        refreshBtn.disabled = false;
    }
}

/**
 * Mostra un messaggio di stato
 */
function showStatus(message, type) {
    uploadStatus.className = `status-message ${type}`;
    uploadStatus.textContent = message;
    uploadStatus.style.display = 'block';
    
    if (type === 'success') {
        setTimeout(() => {
            uploadStatus.style.display = 'none';
        }, 5000);
    }
}
