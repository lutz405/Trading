import json, re, sys
from pathlib import Path

root = Path(r"C:\Users\USER\Documents\GitHub\Trading")
doc = root / "docs" / "aud04b_model_provenance_v3_design.md"
t = doc.read_text(encoding="utf-8")

blocks = re.findall(r"```json\n(.*?)```", t, re.S)
metrics = json.loads(blocks[1])

val = metrics["partitions"]["validation"]
test = metrics["partitions"]["test"]

# Add class_counts to both partitions
val["class_counts"] = [350, 255, 247]
test["class_counts"] = [350, 255, 247]

print(f"Set validation class_counts: {val['class_counts']}")
print(f"Set test class_counts: {test['class_counts']}")

# Verify the ce validation cm row sums and accuracy
ce_cm = val["models"]["calibrated_ensemble"]["confusion_matrix"]
print(f"ce cm: {ce_cm}")
rs = [sum(r) for r in ce_cm]
print(f"ce cm row_sums: {rs}")
diag = ce_cm[0][0] + ce_cm[1][1] + ce_cm[2][2]
acc = round(diag / sum(rs), 4)
print(f"ce cm accuracy: {acc}")
val["models"]["calibrated_ensemble"]["accuracy"] = acc
print(f"Set ce validation accuracy: {acc}")

new_metrics_json = json.dumps(metrics, indent=2, ensure_ascii=False)
print(f"New metrics size: {len(new_metrics_json)} chars")

# Replace block 2 in the document
lines = t.splitlines()

state = 0
block1_start = block1_end = block2_start = block2_end = None
for i, line in enumerate(lines):
    if state == 0 and line.startswith("```json"):
        state = 1
        block1_start = i
    elif state == 1 and line.startswith("```"):
        state = 2
        block1_end = i
    elif state == 2 and line.startswith("```json"):
        state = 3
        block2_start = i
    elif state == 3 and line.startswith("```"):
        state = 4
        block2_end = i
        break

print(f"Block 2 positions: lines {block2_start+1} to {block2_end}")

new_block2 = ["```json"] + new_metrics_json.splitlines() + ["```"]
new_lines = lines[:block2_start] + new_block2 + lines[block2_end+1:]

output = root / "docs" / "aud04b_model_provenance_v3_design.md"
output.write_text("\n".join(new_lines), encoding="utf-8")
print("Written updated document")

# Verify
new_blocks = re.findall(r"```json\n(.*?)```", "\n".join(new_lines), re.S)
if len(new_blocks) >= 2:
    m = json.loads(new_blocks[1])
    tc = m["partitions"]["test"].get("class_counts")
    vc = m["partitions"]["validation"].get("class_counts")
    print(f"\nVerified test class_counts: {tc}")
    print(f"Verified val class_counts: {vc}")
    print(f"Verified test ce row_sums: {[sum(r) for r in m['partitions']['test']['models']['calibrated_ensemble']['confusion_matrix']]}")
    print(f"Verified val ce row_sums: {[sum(r) for r in m['partitions']['validation']['models']['calibrated_ensemble']['confusion_matrix']]}")
    print(f"Verified val ce accuracy: {m['partitions']['validation']['models']['calibrated_ensemble']['accuracy']}")
    print(f"Verified rf accuracy: {m['partitions']['validation']['models']['rf']['accuracy']}")
    print(f"Verified xgb accuracy: {m['partitions']['validation']['models']['xgb']['accuracy']}")
    print(f"Verified rf cm row_sums: {[sum(r) for r in m['partitions']['validation']['models']['rf']['confusion_matrix']]}")
    print(f"Verified xgb cm row_sums: {[sum(r) for r in m['partitions']['validation']['models']['xgb']['confusion_matrix']]}")
else:
    print("ERROR: could not verify blocks")