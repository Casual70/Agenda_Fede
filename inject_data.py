import json, re, sys

json_file = sys.argv[1] if len(sys.argv) > 1 else 'turni_febbraio_2026.json'

with open(json_file, encoding='utf-8') as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False, indent=12)
json_str = json_str.replace('\n', '\n        ')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Sostituisce il blocco turniDataMock (qualunque sia il commento sopra)
pattern = r'// Dati.*?(?=\n\n        let turniData)'
replacement = f'// Dati aggiornati ({len(data)} giorni) — generati automaticamente da parse_turni.py\n        const turniDataMock = {json_str};'

new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

if new_html == html:
    print("ERRORE: pattern non trovato in index.html.")
    sys.exit(1)
else:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"index.html aggiornato con {len(data)} giorni.")

