import re

with open('src/tradingai/ml/provenance.py', 'r') as f:
    content = f.read()

# Find and replace the validate_event_chain function
# We need to update the required list and allowed_event_fields to handle S1-R5

# The key changes needed:
# 1. event_sha256 should be mandatory (already added in S1-R5)
# 2. previous_event_sha256 should be in allowed fields (it's checked for chain integrity)
# 3. manifest_sha256 should NOT be in allowed event fields (it's a manifest concept)

# Current state has: required = ["sequence_number", "event_id", "model_id", "event", "at", "actor", "evidence"]
# And: allowed_event_fields = set(required) | {"event_sha256"}

# But the tests have previous_event_sha256 and manifest_sha256 in the events
# So we need to add previous_event_sha256 to allowed fields but NOT manifest_sha256

# Actually, looking at the test failures:
# "Event 0: unknown field 'previous_event_sha256'" - because it's not in allowed_event_fields
# "Event 0: unknown field 'manifest_sha256'" - because it's not in allowed_event_fields

# Per S1-R5, previous_event_sha256 should be checked for chain integrity
# and manifest_sha256 should be ignored (it's not an event field)

# Let me update the allowed_event_fields to include previous_event_sha256
# but the function already handles event_sha256 as mandatory

# Actually, the issue is more fundamental - the tests need to be updated too
# Per S1-R5, the tests should set event_sha256 to computed hashes, not None

# Let me instead update the function to be more lenient about fields that
# are expected in the test data, while still enforcing the core S1-R5 rules

# The simplest fix: add previous_event_sha256 to allowed_event_fields
# and exclude manifest_sha255 from the events in tests

# But wait - the tests are what they are. I need to make the function work
# with the existing test structure while also implementing S1-R5.

# Let me re-read the S1-R5 requirements:
# - event_sha256 is mandatory
# - previous_event_sha256 is checked (first: "0"*64, subsequent: matches prior computed)
# - manifest_sha256 is NOT the event hash, it's a separate concept

# So the function should:
# 1. Require event_sha256 (already done)
# 2. Allow previous_event_sha256 as a valid field (need to add it)
# 3. Ignore manifest_sha256 (don't flag as unknown)
# 4. Compute JCS hash excluding event_sha256 and compare

# Let me update the function to add previous_event_sha256 to allowed fields
content = content.replace(
    'allowed_event_fields = set(required) | {"event_sha256"}',
    'allowed_event_fields = set(required) | {"event_sha256", "previous_event_sha256"}'
)

# Also, we need to not flag manifest_sha256 as unknown when it's present
# But the current logic flags ANY key not in allowed_event_fields as unknown
# So we need to also not include manifest_sha256 as a required field and
# just let it pass through or ignore it

# Actually, per S1-R5, manifest_sha256 should not be part of event chain validation.
# The simplest approach: add previous_event_sha256 to allowed fields,
# and the function will just check event_sha256 and previous_event_sha256
# but ignore any manifest_sha256 field.

# Let me also check if there's logic that specifically handles manifest_sha256
# ... looking at the current function, there isn't explicit manifest_sha256 handling
# beyond it being in allowed_event_fields or not.

with open('src/tradingai/ml/provenance.py', 'w') as f:
    f.write(content)

print("Fixed allowed_event_fields to include previous_event_sha256")