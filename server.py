"""
Server locale per Agenda Turni.
Avvia con:  python server.py
Poi apri:   http://localhost:5000
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess, sys, os, json

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

PYTHON  = sys.executable
BASE    = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return send_file(os.path.join(BASE, 'index.html'))

@app.route('/api/status')
def status():
    return jsonify({'ok': True})

@app.route('/api/parse', methods=['POST'])
def parse():
    data     = request.get_json()
    pdf_name = (data or {}).get('pdfName', '').strip()

    if not pdf_name:
        return jsonify({'error': 'Nome PDF mancante'}), 400

    pdf_path = os.path.join(BASE, pdf_name)
    if not os.path.exists(pdf_path):
        return jsonify({'error': f'File non trovato nella cartella: {pdf_name}'}), 404

    # 1. Esegui il parser
    r1 = subprocess.run(
        [PYTHON, os.path.join(BASE, 'parse_turni.py'), pdf_name],
        capture_output=True, text=True, cwd=BASE
    )
    print("=== PARSER STDOUT ===")
    print(r1.stdout)
    print("=== PARSER STDERR ===")
    print(r1.stderr)
    if r1.returncode != 0:
        return jsonify({'error': 'Errore nel parser', 'details': r1.stderr}), 500

    # Ricava il nome del JSON dall'output del parser (es. "Salvato in turni_febbraio_2026.json (28 giorni)")
    json_file = None
    for line in r1.stdout.splitlines():
        if 'Salvato in' in line:
            # Prende solo la parte fino al primo spazio dopo il .json
            part = line.split('Salvato in')[-1].strip()
            json_file = part.split(' ')[0]   # es. "turni_febbraio_2026.json"
            break

    if not json_file:
        return jsonify({'error': 'Il parser non ha prodotto un file JSON'}), 500

    # 2. Inietta il JSON in index.html
    r2 = subprocess.run(
        [PYTHON, os.path.join(BASE, 'inject_data.py'), json_file],
        capture_output=True, text=True, cwd=BASE
    )
    if r2.returncode != 0:
        return jsonify({'error': "Errore nell'iniezione", 'details': r2.stderr}), 500

    # 3. Leggi il JSON generato e restituiscilo al browser
    json_path = os.path.join(BASE, json_file)
    with open(json_path, encoding='utf-8') as f:
        turni = json.load(f)

    return jsonify({
        'success'  : True,
        'giorni'   : len(turni),
        'jsonFile' : json_file,
        'data'     : turni
    })

if __name__ == '__main__':
    print("=" * 50)
    print("  Server Agenda Turni avviato!")
    print("  Apri: http://localhost:8080")
    print("=" * 50)
    app.run(host='127.0.0.1', port=8080, debug=False)
