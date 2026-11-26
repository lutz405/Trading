import re

with open('tests/test_provenance.py', 'r') as f:
    content = f.read()

# Fix test_valid_chain_single_model - second event's previous_event_sha256
# should be the computed hash of the first event, not "0" * 64
old_test1 = '''    def test_valid_chain_single_model(self):
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

# For the first event chain, the second event's previous_event_sha256
# should be the computed hash of the first event's (excluding event_sha256)
# Since the first event has event_sha256 set to its computed hash,
# the second event should have previous_event_sha256 set to that hash.

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
                # previous_event_sha256 must match the computed event_sha256 of
                # the first event (which is the JCS hash excluding event_sha256)
                "previous_event_sha256": None,  # Will be set below
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
        # For chain integrity: the second event's previous_event_sha256 must equal
        # the first event's computed event_sha256.
        first_event_copy = {k: v for k, v in events[0].items() if k != "event_sha256"}
        first_computed = sha256_canonical(first_event_copy)
        events[0]["event_sha256"] = first_computed
        events[1]["previous_event_sha256"] = first_computed
        events[1]["event_sha256"] = sha256_canonical({k: v for k, v in events[1].items() if k != "event_sha256"})
    
        errors = validate_event_chain(events)
        assert errors == [], f"Expected no errors for valid chain, got: {errors}"'''

content = content.replace(old_test1, new_test1)

# Fix test_two_intercalated_models similarly
old_test2 = '''    def test_two_intercalated_models(self):
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
                # previous_event_sha256 must match the computed event_sha256 of the
                # prior event in the same model chain (model mdl_01JQ8Z...)
                "previous_event_sha256": None,  # Will be set below
                "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9L1",
                "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
                "event": "validated",
                "at": "2026-11-25T12:00:00Z",
                "actor": "verifier",
                "evidence": None,
            },
            {
                "sequence_number": 2,
                # previous_event_sha256 must match the computed event_sha256 of the
                # prior event in the same model chain (model mdl_02JQ8Z...)
                "previous_event_sha256": None,  # Will be set below
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
        # For model mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W (events 0 and 2):
        first_event_0_copy = {k: v for k, v in events[0].items() if k != "event_sha256"}
        first_computed_0 = sha256_canonical(first_event_0_copy)
        events[0]["event_sha256"] = first_computed_0
        events[2]["previous_event_sha256"] = first_computed_0
        events[2]["event_sha256"] = sha256_canonical({k: v for k, v in events[2].items() if k != "event_sha256"})
        # For model mdl_02JQ8Z3K4M5N6P7Q8R9S0T1V2X (events 1 and 3):
        first_event_1_copy = {k: v for k, v in events[1].items() if k != "event_sha256"}
        first_computed_1 = sha256_canonical(first_event_1_copy)
        events[1]["event_sha256"] = first_computed_1
        events[3]["previous_event_sha256"] = first_computed_1
        events[3]["event_sha256"] = sha256_canonical({k: v for k, v in events[3].items() if k != "event_sha256"})
    
        errors = validate_event_chain(events)
        # Should have no errors since sequences are independent per model_id
        assert len(errors) == 0, f"Expected no errors for intercalated models, got: {errors}"'''

content = content.replace(old_test2, new_test2)

with open('tests/test_provenance.py', 'w') as f:
    f.write(content)

print("Fixed test previous_event_sha256 values for S1-R5 chain integrity")