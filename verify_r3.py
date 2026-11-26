from pathlib import Path

t = Path(r'C:\Users\USER\Documents\GitHub\Trading\docs\aud04b_model_provenance_v3_design.md').read_text(encoding='utf-8')

# Check the sequence rule in 7.8.3 more carefully
idx783 = t.find('### 7.8.3')
if idx783 >= 0:
    # Print the full section 7.8.3
    section = t[idx783:idx783+800]
    print('7.8.3 section found at position', idx783)
    print()
    print(section)
    
    # Check for the specific rule patterns
    patterns = [
        'sequence_number == previous.sequence_number + 1',
        'sequence_number == previous_event_sha256',
        'secua incrementa',
        'crece en exactamente 1'
    ]
    for p in patterns:
        found = p in section
        print(f'  Pattern "{p}": {"FOUND" if found else "NOT FOUND"}')
else:
    print('7.8.3 section NOT found')