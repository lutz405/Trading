import json, re
from pathlib import Path

doc = Path(r"C:\Users\USER\Documents\GitHub\Trading\docs\aud04b_model_provenance_v3_design.md").read_text(encoding="utf-8")

# Search for key phrases
for phrase in ["7.8.6", "7.8.5", "7.8.4", "anclaje externo", "integrity-only", "8.3 Política", "8.1 Contrato"]:
    positions = [m.start() for m in re.finditer(phrase, doc)]
    print(f"'{phrase}': {len(positions)} positions")
    if positions:
        print(f"  First at: {positions[0]}")
        print(f"  Context: {doc[positions[0]:positions[0]+120]}")
'@ | cd C:\TradingAI_BTC && python -B