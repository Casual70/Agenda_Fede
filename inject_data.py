import json, re, sys, os

if len(sys.argv) < 2:
    print("Uso: python inject_data.py file1.json [file2.json ...]")
    sys.exit(1)

MESI_IT = {
    'gennaio':1,'febbraio':2,'marzo':3,'aprile':4,'maggio':5,'giugno':6,
    'luglio':7,'agosto':8,'settembre':9,'ottobre':10,'novembre':11,'dicembre':12
}

def mese_order(mese_key):
    p = mese_key.split('_')
    if len(p) < 2:
        return 999999
    m = MESI_IT.get(p[0].lower(), 99)
    y = int(p[1]) if p[1].isdigit() else 9999
    return y * 100 + m

all_data = []
all_mesi_info = []

for json_file in sys.argv[1:]:
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)
    base  = os.path.splitext(os.path.basename(json_file))[0]  # es. turni_maggio_2026
    parts = base.split('_')                                    # ['turni', 'maggio', '2026']
    mese_key   = f"{parts[1]}_{parts[2]}" if len(parts) >= 3 else "sconosciuto"
    mese_label = f"{parts[1].upper()} {parts[2]}" if len(parts) >= 3 else "?"
    for day in data:
        day['mese'] = mese_key
    all_data.extend(data)
    if mese_key not in [x[0] for x in all_mesi_info]:
        all_mesi_info.append((mese_key, mese_label))

# Ordina per mese poi per id giorno
all_data.sort(key=lambda d: (mese_order(d.get('mese', '')), d.get('id', 0)))

# Etichetta display: es. "MAGGIO 2026 — GIUGNO 2026"
all_mesi_info.sort(key=lambda x: mese_order(x[0]))
mese_display = ' \u2014 '.join(m[1] for m in all_mesi_info)

json_str = json.dumps(all_data, ensure_ascii=False, indent=12)
json_str = json_str.replace('\n', '\n        ')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# Sostituisce il blocco turniDataMock + turniMeseLabel
pattern = r'// Dati.*?(?=\n\n        let turniData)'
replacement = (
    f'// Dati aggiornati ({len(all_data)} giorni) \u2014 generati automaticamente da parse_turni.py\n'
    f'        let turniDataMock = {json_str};\n'
    f'        let turniMeseLabel = "{mese_display}"; // aggiornato dinamicamente da elaboraPdf / inject_data.py'
)

if not re.search(pattern, html, re.DOTALL):
    print("ERRORE: pattern non trovato in index.html.")
    sys.exit(1)

new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print(f"index.html aggiornato con {len(all_data)} giorni \u2014 mesi: {mese_display}")

