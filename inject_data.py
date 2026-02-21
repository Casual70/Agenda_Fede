import json, re

with open('turni_febbraio_2026.json', encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False, indent=12)
# Indenta per il codice JS
json_str = json_str.replace('\n', '\n        ')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Sostituisce il blocco turniDataMock
pattern = r'// Dati di esempio.*?(?=\n\n        let turniData)'
replacement = f'// Dati completi Febbraio 2026 (generati da parse_turni.py)\n        const turniDataMock = {json_str};'

new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

if new_html == html:
    print("ERRORE: pattern non trovato! Nessuna modifica.")
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"index.html aggiornato con {len(data)} giorni.")
