import re

with open('tests/test_provenance.py', 'r') as f:
    content = f.read()

# Update test_valid_chain_single_model - set event_sha256 to computed hash, remove manifest_sha256
old_test1 = '''    def test_valid_chain_single_model(self):
        """Test a valid event chain for a single model.

        Per R7, all events in a chain must have previous_event_sha256 == "0" * 64
        (the genesis hash). Sequences increment by 1.
        manifest_sha256 is set to a computed hash (not None) per S1-R4 to
        demonstrate that the field is properly populated; the test focuses on
        sequence continuity and ordering.
        """
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "manifest_sha256": None,
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9L0",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "validated",
                "at": "2026-11-25T11:00:00Z",
                "manifest_sha256": None,
                "actor": "verifier",
                "evidence": None,
            },
        ]
        # Compute proper JCS canonical hashes and set manifest_sha256
        # Per S1-R4: do not use None to omit cryptographic verification
        for event in events:
            event_copy = {k: v for k, v in event.items() if k != "event_sha256"}
            computed = sha256_canonical(event_copy)
            event["manifest_sha256"] = computed
        
        errors = validate_event_chain(events)
        assert errors == [], f"Expected no errors for valid chain, got: {errors}"'''

new_test1 = '''    def test_valid_chain_single_model(self):
        """Test a valid event chain for a single model.

        Per R7, all events in a chain must have previous_event_sha256 == "0" * 64
        (the genesis hash). Sequences increment by 1.
        Per S1-R5: event_sha256 is mandatory and must match the JCS canonical hash.
        The test focuses on sequence continuity and ordering, with properly
        computed event_sha256 values.
        """
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9L0",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "validated",
                "at": "2026-11-25T11:00:00Z",
                "actor": "verifier",
                "evidence": None,
            },
        ]
        # Compute proper JCS canonical hashes (excluding event_sha256) and set event_sha256
        # Per S1-R5: do not use manifest_sha256 to omit cryptographic verification.
        # Set event_sha256 to the computed hash for each event.
        for event in events:
            event_copy = {k: v for k, v in event.items() if k != "event_sha256"}
            computed = sha256_canonical(event_copy)
            event["event_sha256"] = computed
        
        errors = validate_event_chain(events)
        assert errors == [], f"Expected no errors for valid chain, got: {errors}"'''

content = content.replace(old_test1, new_test1)

# Update test_two_intercalated_models similarly
old_test2 = '''    def test_two_intercalated_models(self):
        """Test two models interleaved in the same event list.

        Sequences are independent per model_id. All events have
        previous_event_sha256 == "0" * 64 (genesis).
        manifest_sha256 is set to a valid computed hash (not None) per S1-R4.
        """
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "manifest_sha256": None,
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9L0",
                "model_id": "mdl_02JQ8Z3K4M5N6P7Q8R9S0T1V2X",
                "event": "sealed",
                "at": "2026-11-25T10:30:00Z",
                "manifest_sha256": None,
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9L1",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "validated",
                "at": "2026-11-25T12:00:00Z",
                "manifest_sha256": None,
                "actor": "verifier",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9L2",
                "model_id": "mdl_02JQ8Z3K4M5N6P7Q8R9S0T1V2X",
                "event": "validated",
                "at": "2026-11-25T13:00:00Z",
                "manifest_sha256": None,
                "actor": "verifier",
                "evidence": None,
            },
        ]
        # Compute proper JCS canonical hashes and set manifest_sha256
        for event in events:
            event_copy = {k: v for k, v in event.items() if k != "event_sha256"}
            computed = sha256_canonical(event_copy)
            event["manifest_sha256"] = computed
        
        errors = validate_event_chain(events)
        # Should have no errors since sequences are independent per model_id
        assert len(errors) == 0, f"Expected no errors for intercalated models, got: {errors}"'''

new_test2 = '''    def test_two_intercalated_models(self):
        """Test two models interleaved in the same event list.

        Sequences are independent per model_id. All events have
        previous_event_sha256 == "0" * 64 (genesis).
        Per S1-R5: event_sha256 is mandatory and must match the JCS canonical hash.
        The test demonstrates independent chains per model_id with properly
        computed event_sha256 values.
        """
        events = [
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "sealed",
                "at": "2026-11-25T10:00:00Z",
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 1,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9L0",
                "model_id": "mdl_02JQ8Z3K4M5N6P7Q8R9S0T1V2X",
                "event": "sealed",
                "at": "2026-11-25T10:30:00Z",
                "actor": "pipeline",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9L1",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "validated",
                "at": "2026-11-25T12:00:00Z",
                "actor": "verifier",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                "previous_event_sha256": "0" * 64,
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9L2",
                "model_id": "mdl_02JQ8Z3K4M5N6P7Q8R9S0T1V2X",
                "event": "validated",
                "at": "2026-11-25T13:00:00Z",
                "actor": "verifier",
                "evidence": None,
            },
        ]
        # Compute proper JCS canonical hashes (excluding event_sha256) and set event_sha256
        # Per S1-R5: do not use manifest_sha256 to omit cryptographic verification.
        for event in events:
            event_copy = {k: v for k, v in event.items() if k != "event_sha256"}
            computed = sha256_canonical(event_copy)
            event["event_sha256"] = computed
        
        errors = validate_event_chain(events)
        # Should have no errors since sequences are independent per model_id
        assert len(errors) == 0, f"Expected no errors for intercalated models, got: {errors}"'''

content = content.replace(old_test2, new_test2)

with open('tests/test_provenance.py', 'w') as f:
    f.write(content)

print("Updated test file with S1-R5 event_sha256 handling")