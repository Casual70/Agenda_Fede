import json, re, sys, os

json_file = sys.argv[1] if len(sys.argv) > 1 else 'turni_febbraio_2026.json'

with open(json_file, encoding='utf-8') as f:
    data = json.load(f)

# Deriva il label "MESE ANNO" dal nome del file (es. turni_marzo_2026.json → MARZO 2026)
base  = os.path.splitext(os.path.basename(json_file))[0]   # turni_marzo_2026
parts = base.split('_')                                      # ['turni', 'marzo', '2026']
mese_label = f"{parts[1].upper()} {parts[2]}" if len(parts) >= 3 else "?"

json_str = json.dumps(data, ensure_ascii=False, indent=12)
json_str = json_str.replace('\n', '\n        ')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Sostituisce il blocco turniDataMock + turniMeseLabel (qualunque sia il commento sopra)
pattern = r'// Dati.*?(?=\n\n        let turniData)'
replacement = (
    f'// Dati aggiornati ({len(data)} giorni) \u2014 generati automaticamente da parse_turni.py\n'
    f'        let turniDataMock = {json_str};\n'
    f'        let turniMeseLabel = "{mese_label}"; // aggiornato dinamicamente da elaboraPdf / inject_data.py'
)

if not re.search(pattern, html, re.DOTALL):
    print("ERRORE: pattern non trovato in index.html.")
    sys.exit(1)

new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print(f"index.html aggiornato con {len(data)} giorni — mese: {mese_label}")

