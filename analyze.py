with open('src/tradingai/ml/provenance.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(500, 515):
    if i < len(lines):
        print(f'Line {i+1}: {lines[i][:60]}')
PYEOF