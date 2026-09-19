"""Tests for OddsHawk auth hash construction."""

import hashlib

from oddshawk_sdk import generate_hash
from oddshawk_sdk import hashing as hashing_mod


def test_generate_hash_matches_sha256_plus_hex_time():
    key = "test-password"
    ts = 1_714_000_000
    expected = hashlib.sha256(f"{key}{ts}".encode("utf-8")).hexdigest() + format(ts, "x")
    assert generate_hash(key, timestamp=ts) == expected


def test_generate_hash_uses_current_time_when_omitted(monkeypatch):
    monkeypatch.setattr(hashing_mod.time, "time", lambda: 1_600_000_000.9)
    result = generate_hash("k")
    assert result.endswith(format(1_600_000_000, "x"))
    assert len(result) == 64 + len(format(1_600_000_000, "x"))


def test_generate_hash_wire_shape():
    result = generate_hash("secret", timestamp=42)
    assert result[:64].isalnum()
    assert result[64:] == "2a"
