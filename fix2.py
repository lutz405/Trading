with open('src/tradingai/ml/provenance.py', 'r') as f:
    content = f.read()

old = """        # unknown fields, event type, etc.) before chain che
        errors.append(f"Event {idx}: {e}")        # Basi
        required = ["sequence_number", "event_id", "model_id"""
new = """        # unknown fields, event type, etc.) before chain che
        errors.append(f"Event {idx}: {e}")
        required = ["sequence_number", "event_id", "model_id", "event", "at", "actor", "evidence"]"""

if old in content:
    content = content.replace(old, new)
    with open('src/tradingai/ml/provenance.py', 'w') as f:
        f.write(content)
    print('Fixed')
else:
    print('Old string not found')