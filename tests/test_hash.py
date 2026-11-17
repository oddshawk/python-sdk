"""Tests for OddsHawk auth hash construction."""

import hashlib

import pytest

from oddshawk_sdk import generate_hash
from oddshawk_sdk import hashing as hashing_mod

# Fixed digests of f"{key}{TS}" encoded as UTF-8. Each key rules out a different encoding: "clé"
# is representable in latin-1, and "日本" is not, so a drift to a single-byte codec changes the
# first digest and raises on the second; both differ under utf-16.
TS = 1_714_000_000
UTF8_KEY_DIGESTS = [
    ("clé", "f54c83413e09be083bfe9621ef18a7d7024ad3cf198d6b800ae9dd1dd80ac86d"),
    ("日本", "d48b17508960cd88b91c5f286113f2be897077da60f8a3226be9dc80a128fc33"),
]


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


@pytest.mark.parametrize(("key", "digest"), UTF8_KEY_DIGESTS)
def test_generate_hash_hashes_the_key_as_utf_8(key, digest):
    assert generate_hash(key, timestamp=TS)[:64] == digest
