"""
test_forge_time_at_v1_0_1.py — P16 Time test suite, 1.0.1

Function:
    Executable expression of SPEC.md 1.0.0 as changed by SPEC_V1_0_1.md.
    The 1.0.0 suite (archive/1.0.0/test_forge_time.py, byte-identical)
    less test 6, the agreement check against the-full-stack's forge_core:
    James, 2026-11-18, the-full-stack was for reference only and never a
    layer of the Legacy. Numbering kept, so 6 is the new no-reach check.

Functions in this file (pytest-collected):
    1. test_timestamp_table
    2. test_scp_id_table
    3. test_parse_errors_and_is_never_raises
    4. test_format_and_round_trip
    5. test_utc_now
    6. test_never_reaches_the_full_stack
    7. test_capsule_names_this_spec
    8. test_seal_capsule_verifies_under_p3
    9. test_capsule_v2_pins_both_specs

Helpers:
    9. VALID_TS, INVALID_TS, VALID_IDS, INVALID_IDS — the tables

Layer:    P16 — Time
Spec:     SPEC.md 1.0.0 + SPEC_V1_0_1.md
Licence:  MSL-1.0
Author:   James Gilbert (Giblets Forge)
"""

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import forge_time
import seal_capsule

HERE = os.path.dirname(os.path.abspath(__file__))

# 9. the tables
VALID_TS = ["2026-11-14T17:00:00Z", "1970-01-01T00:00:00Z", "2024-02-29T23:59:59Z", "9999-12-31T23:59:59Z"]
INVALID_TS = ["2026-11-14T17:00:00Z\n", "2026-11-14T17:00:00z", "2026-11-14 17:00:00Z", "2026-11-14T17:00:00",
              "2026-11-14T17:00:00+00:00", "2026-11-14T17:00:00.5Z", "2026-02-30T00:00:00Z", "2025-02-29T00:00:00Z",
              "2026-11-14T24:00:00Z", "2026-13-01T00:00:00Z", "26-11-14T17:00:00Z", " 2026-11-14T17:00:00Z", ""]
VALID_IDS = ["forge-stack/primitive/p16-time-v1", "a-v0", "forge-stack/governance-v6", "x/y/z-1-v12"]
INVALID_IDS = ["forge-stack/primitive/p16-time-v1\n", "Forge/x-v1", "forge_stack/x-v1", "forge-stack/x", "x-v",
               "/x-v1", "x//y-v1", "x/y-v1/", "x.y-v1", "", "x y-v1"]


# 1. test_timestamp_table
def test_timestamp_table():
    for s in VALID_TS:
        assert forge_time.is_iso_utc(s), s
        assert forge_time.ISO_UTC_RE.fullmatch(s), s
    for s in INVALID_TS:
        assert not forge_time.is_iso_utc(s), repr(s)


# 2. test_scp_id_table
def test_scp_id_table():
    for s in VALID_IDS:
        assert forge_time.is_ratified_scp_id(s), s
    for s in INVALID_IDS:
        assert not forge_time.is_ratified_scp_id(s), repr(s)


# 3. test_parse_errors_and_is_never_raises
def test_parse_errors_and_is_never_raises():
    for bad in (None, 12, b"2026-11-14T17:00:00Z", datetime.now(timezone.utc)):
        with pytest.raises(TypeError):
            forge_time.parse_iso_utc(bad)
        assert forge_time.is_iso_utc(bad) is False
        assert forge_time.is_ratified_scp_id(bad) is False
    for bad in INVALID_TS:
        with pytest.raises(ValueError):
            forge_time.parse_iso_utc(bad)
    d = forge_time.parse_iso_utc("2026-11-14T17:00:05Z")
    assert d == datetime(2026, 11, 14, 17, 0, 5, tzinfo=timezone.utc) and d.utcoffset() == timedelta(0)


# 4. test_format_and_round_trip
def test_format_and_round_trip():
    assert forge_time.format_iso_utc(datetime(2026, 11, 14, 17, 0, 5)) == "2026-11-14T17:00:05Z"
    plus_one = timezone(timedelta(hours=1))
    assert forge_time.format_iso_utc(datetime(2026, 11, 14, 18, 0, 5, tzinfo=plus_one)) == "2026-11-14T17:00:05Z"
    assert forge_time.format_iso_utc(datetime(2026, 11, 14, 17, 0, 5, 999999, tzinfo=timezone.utc)) == \
        "2026-11-14T17:00:05Z"
    for s in VALID_TS:
        assert forge_time.format_iso_utc(forge_time.parse_iso_utc(s)) == s


# 5. test_utc_now
def test_utc_now():
    s = forge_time.utc_now()
    assert forge_time.is_iso_utc(s)
    assert abs(forge_time.parse_iso_utc(s).timestamp() - time.time()) < 2


# 6. test_never_reaches_the_full_stack
def test_never_reaches_the_full_stack():
    """SPEC_V1_0_1 §1: nothing here imports forge_core or looks for the-full-stack."""
    assert "forge_core" not in sys.modules
    for name in ("forge_time.py", "seal_capsule.py", "conftest.py"):
        with open(os.path.join(HERE, name), encoding="utf-8") as f:
            text = f.read()
        assert "import forge_core" not in text, name
        assert '"the-full-stack"' not in text, name


# 7. test_capsule_names_this_spec
def test_capsule_names_this_spec():
    with open(os.path.join(HERE, "sc", "p16-time-v1.sc.json"), encoding="utf-8") as f:
        capsule = json.load(f)
    with open(os.path.join(HERE, "SPEC.md"), "rb") as f:
        spec_sha = hashlib.sha256(f.read()).hexdigest()
    assert capsule["scp_id"] == "forge-stack/primitive/p16-time-v1"
    assert forge_time.is_ratified_scp_id(capsule["scp_id"])
    assert capsule["inherits"] == "forge-stack/governance-v6"
    assert forge_time.is_iso_utc(capsule["created"])
    assert capsule["declaration"]["layer"] == "P16" and capsule["declaration"]["module"] == "forge_time.py"
    assert capsule["declaration"]["spec_sha256"] == spec_sha
    sig = capsule["signature"]
    assert sig is None or (isinstance(sig, dict) and sig.get("algorithm") == "Ed25519")


# 8. test_seal_capsule_verifies_under_p3
def test_seal_capsule_verifies_under_p3(tmp_path):
    with open(os.path.join(HERE, "sc", "p16-time-v1.sc.json"), encoding="utf-8") as f:
        capsule = json.load(f)
    path = tmp_path / "copy.sc.json"
    path.write_text(json.dumps(capsule, indent=2) + "\n", encoding="utf-8")
    key = Ed25519PrivateKey.generate()
    seal_capsule.seal(str(path), key)
    sealed = json.loads(path.read_text(encoding="utf-8"))
    import freeze_v2
    assert freeze_v2.verify_frozen_capsule(sealed, key.public_key())
    assert sealed["declaration"] == capsule["declaration"]
    assert b"\r" not in path.read_bytes()


# 9. test_capsule_v2_pins_both_specs
def test_capsule_v2_pins_both_specs():
    """The 1.0.1 capsule names SPEC_V1_0_1.md and SPEC.md by hash, supersedes v1, inherits nothing."""
    with open(os.path.join(HERE, "sc", "p16-time-v2.sc.json"), encoding="utf-8") as f:
        cap = json.load(f)
    d = cap["declaration"]
    for name, key in (("SPEC_V1_0_1.md", "spec_sha256"), ("SPEC.md", "base_spec_sha256")):
        with open(os.path.join(HERE, name), "rb") as f:
            assert d[key] == hashlib.sha256(f.read()).hexdigest(), name
    assert (cap["scp_id"], d["spec_version"], d["supersedes"], cap["inherits"]) ==         ("forge-stack/primitive/p16-time-v2", "1.0.1", "forge-stack/primitive/p16-time-v1", None)
    assert forge_time.is_iso_utc(cap["created"]) and "derived_from" not in d
    sig = cap["signature"]
    assert sig is None or (isinstance(sig, dict) and sig.get("algorithm") == "Ed25519")
