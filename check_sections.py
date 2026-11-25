import json, re
from pathlib import Path

root = Path(r"C:\Users\USER\Documents\GitHub\Trading")
doc = root / "docs" / "aud04b_model_provenance_v3_design.md"
t = doc.read_text(encoding="utf-8")

# Find "## 8. Loader" section
idx = t.find("## 8. Loader")
if idx >= 0:
    idx2 = t.find("## 9", idx+1)
    if idx2 < 0:
        idx2 = len(t)
    loader_section = t[idx:idx2]
    print("§8. Loader size:", len(loader_section))
    print("First 200:", loader_section[:200])
    
    # Find "8.3" within
    idx83 = loader_section.find("8.3")
    if idx83 >= 0:
        print("\n8.3 within loader section:")
        print(loader_section[idx83:idx83+500])
    else:
        print("\n8.3 NOT found in §8. Loader")
else:
    print("## 8. Loader NOT found")
    
# Also check if 8.3 exists anywhere
print("\n'8.3' in doc overall:", "8.3" in t)
# Find all occurrences of 8.3
positions = [m.start() for m in re.finditer(r"8\.3", t)]
print("All '8.3' positions:", positions[:10])
# Show context around each
for p in positions[:3]:
    print("Context at", p, ":", t[max(0,p-20):p+50])