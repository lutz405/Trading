import json, re
from pathlib import Path

root = Path(r"C:\Users\USER\Documents\GitHub\Trading")
doc = root / "docs" / "aud04b_model_provenance_v3_design.md"
t = doc.read_text(encoding="utf-8")

# Check JSON blocks
blocks = re.findall(r"```json\n(.*?)```", t, re.S)
print("JSON blocks:", len(blocks))
for i, b in enumerate(blocks, 1):
    try:
        json.loads(b)
        print("Block", i, "OK")
    except:
        print("Block", i, "FAIL")

# Check sections
print("7.8.6 in doc:", "7.8.6" in t)
print("7.8.5 in doc:", "7.8.5" in t)

# Find the §7.8.5 section and add truncation/external anchoring content
# Find 7.8.5
idx5 = t.find("### 7.8.5 Política ante eventos duplicados o fuera de orden")
if idx5 >= 0:
    # Get the section content
    idx5_end = t.find("\n### ", idx5+1)
    if idx5_end < 0:
        idx5_end = t.find("\n---", idx5+1)
    current_785 = t[idx5:idx5_end]
    print("\n§7.8.5 current length:", len(current_785))
else:
    print("§7.8.5 not found")

# Find §7.8.6
idx6 = t.find("### 7.8.6 Anclaje externo y truncamiento")
if idx6 < 0:
    idx6 = t.find("7.8.6 Anclaje")
print("§7.8.6 position:", idx6)

# Find §8.3
idx83 = t.find("### 8.3 Política de estado por propósito")
if idx83 >= 0:
    print("\n§8.3 found at position", idx83)
    chunk = t[idx83:idx83+1500]
    print("§8.3 starts:", chunk[:300])
else:
    print("§8.3 not found")
'@ | python -B