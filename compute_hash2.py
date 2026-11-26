import math
import hashlib
import json

def _utf16_sort_key(s):
    encoded = s.encode("utf-16-le")
    units = []
    for i in range(0, len(encoded), 2):
        unit = encoded[i] | (encoded[i + 1] << 8)
        units.append(unit)
    return units

def _jcs_number(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            raise ValueError("NaN and Infinity are not allowed in JCS")
        if value == 0.0:
            if math.copysign(1.0, value) < 0:
                return "-0"
            return "0"
        abs_val = abs(value)
        if abs_val >= 1e21 or (abs_val < 1e-7 and abs_val > 0):
            r = repr(value)
            if "e" in r.lower():
                mantissa, exp_part = r.lower().split("e")
                if exp_part.startswith("+"):
                    exp_sign = "+"
                    exp_digits = exp_part[1:]
                else:
                    exp_sign = exp_part[0] if exp_part[0] in "+-" else "+"
                    exp_digits = exp_part[1:] if exp_sign in "+-" else exp_part
                exp_digits = exp_digits.lstrip("0") or "0"
                if not exp_digits:
                    exp_digits = "0"
                r = f"{mantissa}e{exp_sign}{exp_digits}"
            else:
                r = r.lower()
            return r
        else:
            r = repr(value)
            if r.endswith(".0"):
                if value == int(value):
                    r = r[:-2]
            return r
    raise TypeError(f"Unsupported type: {type(value)}")

def jcs_canonicalize(obj):
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, int):
        if abs(obj) > 2**53:
            pass
        return str(obj)
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            raise ValueError("NaN and Infinity are not allowed in JCS")
        if obj == 0.0:
            if math.copysign(1.0, obj) < 0:
                return "-0"
            return "0"
        abs_val = abs(obj)
        if abs_val >= 1e21 or (abs_val < 1e-6 and abs_val > 0):
            r = repr(obj)
            if "e" in r.lower():
                mantissa, exp_part = r.lower().split("e")
                if exp_part.startswith("+"):
                    exp_sign = "+"
                    exp_digits = exp_part[1:]
                else:
                    exp_sign = exp_part[0] if exp_part[0] in "+-" else "+"
                    exp_digits = exp_part[1:] if exp_sign in "+-" else exp_part
                exp_digits = exp_digits.lstrip("0") or "0"
                if not exp_digits:
                    exp_digits = "0"
                r = f"{mantissa}e{exp_sign}{exp_digits}"
            else:
                r = r.lower()
            return r
        else:
            r = repr(obj)
            if r.endswith(".0") and obj == int(obj) and abs(obj) < 2**53:
                r = r[:-2]
            return r
    if isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    if isinstance(obj, list):
        return "[" + ",".join(jcs_canonicalize(item) for item in obj) + "]"
    if isinstance(obj, dict):
        sorted_keys = sorted(obj.keys(), key=_utf16_sort_key)
        pairs = []
        for key in sorted_keys:
            if not isinstance(key, str):
                raise TypeError("JSON object keys must be strings")
            pairs.append(
                json.dumps(key, ensure_ascii=False, separators=(",", ":"))
                + ":"
                + jcs_canonicalize(obj[key])
            )
        return "{" + ",".join(pairs) + "}"
    raise TypeError(f"Unsupported type: {type(obj)}")

def jcs_canonical_bytes(obj):
    return jcs_canonicalize(obj).encode("utf-8")

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def sha256_canonical(obj):
    return sha256_bytes(jcs_canonical_bytes(obj))

# Test event from test_valid_chain_single_model
event1 = {
    "sequence_number": 1,
    "previous_event_sha256": "0" * 64,
    "event_id": "evt_01JQ8Z4A1B2C3D4E5F6G7H8J9K",
    "model_id": "mdl_01JQ8Z3K4M5N6P7Q8R9S0T1V2W",
    "event": "sealed",
    "at": "2026-11-25T10:00:00Z",
    "manifest_sha256": None,
    "actor": "pipeline",
    "evidence": None,
}

# Approach: remove manifest_sha256 before computing hash, then set it
event1_no_msh = {k: v for k, v in event1.items() if k not in ("event_sha256", "manifest_sha256")}
computed1_no_msh = sha256_canonical(event1_no_msh)
print("Computed hash (without manifest_sha256):", computed1_no_msh)

# Now set manifest_sha256 to the hash computed without it
event1_set_msh = dict(event1)
event1_set_msh["manifest_sha256"] = computed1_no_msh
# Compute hash again, this time excluding event_sha256 but including the new manifest_sha256
event_copy1 = {k: v for k, v in event1_set_msh.items() if k != "event_sha256"}
computed1_back = sha256_canonical(event_copy1)
print("Re-computed hash (with msh set):", computed1_back)
print("Match:", computed1_no_msh == computed1_back)

# Also test: what if manifest_sha256 is set but we exclude it from the hash check?
# The validate_event_chain code excludes only event_sha256, not manifest_sha256
# So if we want the hash to match, we need the circular consistency
print()
print("--- Testing the actual validate_event_chain logic ---")
# With manifest_sha256 set to the hash computed without it:
msh = computed1_no_msh
event_test = dict(event1)
event_test["manifest_sha256"] = msh
event_copy = {k: v for k, v in event_test.items() if k != "event_sha256"}
computed_hash = sha256_canonical(event_copy)
print(f"msh={msh[:16]}..., computed_hash={computed_hash[:16]}...")
print("Check msh != computed_hash:", msh != computed_hash)