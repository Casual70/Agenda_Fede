import pdfplumber
import json
import re
import sys

# Range X di fallback (usati solo se il rilevamento automatico fallisce)
COL_RANGES_DEFAULT = {
    'NOTTE 2': (40,  82),
    'MATT 1':  (82,  117),
    'MATT 2':  (117, 158),
    'CENTR.':  (158, 218),
    'POM 1':   (218, 250),
    'POM 2':   (250, 285),
    'NOTTE 1': (285, 342),
}

COL_RANGES = COL_RANGES_DEFAULT  # viene aggiornato da detect_col_ranges()
RIUNIONE_X_RANGE = (370, 420)    # colonna RIUNIONI E SUPERV.
RIUNIONE_X_RANGE = (370, 420)    # colonna RIUNIONI E SUPERV.

GIORNI_IT = {
    'DO': 'Domenica', 'LU': 'Lunedì', 'MA': 'Martedì',
    'ME': 'Mercoledì', 'GI': 'Giovedì', 'VE': 'Venerdì', 'SA': 'Sabato'
}
MESI_IT = {
    1:'Gennaio', 2:'Febbraio', 3:'Marzo', 4:'Aprile', 5:'Maggio',
    6:'Giugno', 7:'Luglio', 8:'Agosto', 9:'Settembre',
    10:'Ottobre', 11:'Novembre', 12:'Dicembre'
}

def get_col(x):
    for col, (x0, x1) in COL_RANGES.items():
        if x0 <= x < x1:
            return col
    return None

def fmt_time(t):
    return t.replace(',', ':')

def detect_col_ranges(rows_raw):
    """Rileva i range X delle colonne dall'intestazione del PDF (midpoint tra header adiacenti)."""
    TURNO_LABELS = {'NOTTE', 'MATT', 'CENTR.', 'POM'}
    header_row = None
    for _top, rw in rows_raw[:15]:
        if sum(1 for w in rw if w['text'] in TURNO_LABELS) >= 3:
            header_row = rw
            break
    if not header_row:
        return None

    words_sorted = sorted(header_row, key=lambda w: w['x0'])
    col_starts = {}
    for i, w in enumerate(words_sorted):
        if w['text'] == 'CENTR.':
            col_starts['CENTR.'] = w['x0']
        elif w['text'] in {'NOTTE', 'MATT', 'POM'}:
            for j in range(i + 1, min(i + 4, len(words_sorted))):
                nw = words_sorted[j]
                if nw['text'] in {'1', '2'} and nw['x0'] - w['x0'] < 30:
                    col_name = w['text'] + ' ' + nw['text']
                    if col_name not in col_starts:
                        col_starts[col_name] = w['x0']
                    break

    COL_ORDER = ['NOTTE 2', 'MATT 1', 'MATT 2', 'CENTR.', 'POM 1', 'POM 2', 'NOTTE 1']
    present = [(c, col_starts[c]) for c in COL_ORDER if c in col_starts]
    if len(present) < 4:
        return None

    col_ranges = {}
    for i, (col, pos) in enumerate(present):
        left  = present[i-1][1] + (pos - present[i-1][1]) / 2 if i > 0 else pos - 20
        right = pos + (present[i+1][1] - pos) / 2 if i < len(present) - 1 else pos + 80
        col_ranges[col] = (round(left, 1), round(right, 1))
    return col_ranges

# Accetta il nome del PDF come argomento oppure usa il default
pdf_file = sys.argv[1] if len(sys.argv) > 1 else '2602_ TURNI FEBBRAIO 2026 - ORARIO.pdf'

with pdfplumber.open(pdf_file) as pdf:
    page = pdf.pages[0]
    words = page.extract_words()

# Leggi mese e anno dall'intestazione del PDF
mese_num = None
anno = None
for w in words[:20]:
    for num, nome in MESI_IT.items():
        if w['text'] == nome:
            mese_num = num
    if w['text'].isdigit() and len(w['text']) == 4:
        anno = int(w['text'])
if mese_num is None:
    mese_num = 2  # fallback
if anno is None:
    anno = 2026   # fallback
mese_str = MESI_IT[mese_num]

# Raggruppa parole per riga con tolleranza 3px (fix per label "F DO 1" su y leggermente diversi)
rows_raw = []
for w in words:
    placed = False
    for row in rows_raw:
        if abs(row[0] - w['top']) <= 3:
            row[1].append(w)
            placed = True
            break
    if not placed:
        rows_raw.append([w['top'], [w]])
rows_raw.sort(key=lambda r: r[0])

# Rileva le colonne dinamicamente dall'intestazione del PDF
detected = detect_col_ranges(rows_raw)
if detected:
    COL_RANGES = detected
    print(f"Colonne rilevate: { {k: tuple(round(v,1) for v in vv) for k,vv in COL_RANGES.items()} }")
else:
    print('Attenzione: rilevamento colonne fallito, uso range hardcoded')

DAY_ABBR = re.compile(r'^(LU|MA|ME|GI|VE|SA|DO)$')
NUM_PAT   = re.compile(r'^\d{1,2}$')
TIME_PAT  = re.compile(r'^\d{1,2},\d{2}$')
OP_PAT    = re.compile(r'^[A-Z]{2,5}\.?$')
SKIP_WORDS = {'ANNO','MESE','MESI','TURNI','NOTTE','MATT','CENTR','POM','SUPPL',
              'SPEZZ','RIUNIONI','FERIE','SUPERV','GG','N','E','F','R','OP'}

turni_data = []
day_rows = []  # lista di (idx, y, num, abbr)

for idx, (y, rw) in enumerate(rows_raw):
    left = [w for w in rw if w['x0'] < 50]
    texts = [w['text'] for w in left]

    # "F DO 1" — festivo con tolleranza applicata
    if len(texts) >= 3 and texts[0] == 'F' and texts[1] == 'DO' and NUM_PAT.match(texts[2]):
        day_rows.append((idx, y, int(texts[2]), 'DO'))
    # "LU 2", "SA 7" ecc.
    elif len(texts) >= 2 and DAY_ABBR.match(texts[0]) and NUM_PAT.match(texts[1]):
        day_rows.append((idx, y, int(texts[1]), texts[0]))
    # "MA10", "ME11" ecc. (numero appiccicato all'abbreviazione)
    elif len(texts) >= 1 and re.match(r'^(MA|ME|GI|VE|LU|SA)\d{2}$', texts[0]):
        day_rows.append((idx, y, int(texts[0][2:]), texts[0][:2]))

print(f"Trovati {len(day_rows)} giorni: {[d[2] for d in day_rows]}")

# Rileva le y delle righe con "RIUNIONE" nella colonna RIUNIONI E SUPERV.
riunione_ys = []
for _top, rw in rows_raw:
    chars = [w['text'] for w in rw if RIUNIONE_X_RANGE[0] <= w['x0'] <= RIUNIONE_X_RANGE[1]]
    if 'RIUNIONE' in ''.join(chars).upper():
        riunione_ys.append(_top)


# Rileva le y delle righe con "RIUNIONE" nella colonna RIUNIONI E SUPERV.
riunione_ys = []
for _top, rw in rows_raw:
    chars = [w['text'] for w in rw if RIUNIONE_X_RANGE[0] <= w['x0'] <= RIUNIONE_X_RANGE[1]]
    if 'RIUNIONE' in ''.join(chars).upper():
        riunione_ys.append(_top)


for i_day, (row_idx, day_y, day_num, day_abbr) in enumerate(day_rows):
    next_day_y = day_rows[i_day + 1][1] if i_day + 1 < len(day_rows) else day_y + 100
    riunione = any(day_y < ry < next_day_y for ry in riunione_ys)
    next_day_y = day_rows[i_day + 1][1] if i_day + 1 < len(day_rows) else day_y + 100
    riunione = any(day_y < ry < next_day_y for ry in riunione_ys)
    label = f"{GIORNI_IT.get(day_abbr, day_abbr)} {day_num} {mese_str}"

    # Riga operatori: la riga y immediatamente precedente con nomi
    ops_row = None
    for y2, rw in reversed(rows_raw):
        if y2 >= day_y: continue
        if day_y - y2 > 20: break
        op_words = [w for w in rw if OP_PAT.match(w['text'])
                    and w['text'] not in SKIP_WORDS and w['x0'] > 40]
        if op_words:
            ops_row = rw
            break

    # Riga orari: la riga y immediatamente successiva con numeri tipo "0,00"
    time_row = None
    for y2, rw in rows_raw:
        if y2 <= day_y: continue
        if y2 - day_y > 20: break
        tw = [w for w in rw if TIME_PAT.match(w['text'])]
        if tw:
            time_row = rw
            break

    # Mappa operatori per colonna X
    col_ops = {}
    if ops_row:
        for w in ops_row:
            col = get_col(w['x0'])
            if col and OP_PAT.match(w['text']) and w['text'] not in SKIP_WORDS:
                col_ops[col] = w['text']

    # Mappa orari per colonna X, accoppiati (start, end)
    col_times = {}
    if time_row:
        col_vals = {}
        for w in sorted(time_row, key=lambda x: x['x0']):
            if TIME_PAT.match(w['text']):
                col = get_col(w['x0'])
                if col:
                    col_vals.setdefault(col, []).append(w['text'])
        for col, vals in col_vals.items():
            if len(vals) >= 2:
                col_times[col] = f"{fmt_time(vals[0])} - {fmt_time(vals[1])}"
            elif len(vals) == 1:
                col_times[col] = fmt_time(vals[0])

    shifts = []
    for col in COL_RANGES:
        op = col_ops.get(col, '')
        time = col_times.get(col, '')
        if op:
            shifts.append({'name': col, 'op': op, 'time': time})

    turni_data.append({'id': day_num, 'dayLabel': label, 'shifts': shifts, 'riunione': riunione})

# Ordina per giorno
turni_data.sort(key=lambda d: d['id'])

# Post-processing: fix turni con orario incompleto (es. NOTTE 2 giorno 1 = solo "0:00")
NOTTE2_DEFAULT = {'feriale': '0:00 - 9:00', 'festivo': '0:00 - 9:00'}
for d in turni_data:
    for s in d['shifts']:
        if ' - ' not in s['time']:
            if s['name'] == 'NOTTE 2' and s['time'] == '0:00':
                s['time'] = '0:00 - 9:00'

print("\n=== VERIFICA RAPIDA ===")
for d in turni_data:
    print(f"  Giorno {d['id']:2d} ({d['dayLabel'][:15]}): {len(d['shifts'])} turni - {[s['op'] for s in d['shifts']]}")

# Nome file JSON dinamico
json_filename = f'turni_{mese_str.lower()}_{anno or 2026}.json'

with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(turni_data, f, ensure_ascii=False, indent=2)
print(f"Salvato in {json_filename} ({len(turni_data)} giorni)")
