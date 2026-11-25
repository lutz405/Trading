import json, re
from pathlib import Path

root = Path(r"C:\Users\USER\Documents\GitHub\Trading")
doc = root / "docs" / "aud04b_model_provenance_v3_design.md"
t = doc.read_text(encoding="utf-8")

# Check JSON blocks
blocks = __import__('re').findall(r"```json\n(.*?)```", t, __import__('re').S)
print("JSON blocks:", len(blocks))
for i, b in enumerate(blocks, 1):
    try:
        json.loads(b)
        print("Block", i, "OK")
    except:
        print("Block", i, "FAIL")

# Check for key phrases
for phrase in ["integrity-only", "No deserializar", "modo integrity", "authentication", "firma Ed25519"]:
    positions = len(__import__('re').findall(phrase, t, __import__('re').IGNORECASE))
    print(f"'{phrase}': {positions} occurrences")

# Find 7.8.6
idx6 = t.find("7.8.6 Anclaje externo")
if idx6 >= 0:
    print("\n7.8.6 found, content:")
    print(t[idx6:idx6+600])
else:
    print("\n7.8.6 NOT found")

# Find 8.3
positions83 = [m.start() for m in __import__('re').finditer(r"8\.3", t)]
print("\n'8.3' positions:", positions83[:5])
for p in positions83[:3]:
    print("Context at", p, ":", t[max(0,p-30):p+80])
'@ | python -B