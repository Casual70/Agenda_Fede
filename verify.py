import json
with open('turni_febbraio_2026.json', encoding='utf-8') as f:
    data = json.load(f)
for d in data[:4]:
    print(d['dayLabel'])
    for s in d['shifts']:
        name = s['name']
        op = s['op']
        time = s['time']
        print(f'  {name}: {op} ({time})')
    print()
