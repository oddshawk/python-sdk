"""Smoke tests for OddsHawk Python SDK hash / Rest surface (cn-123, updated by cn-127)."""

import hashlib
import time

import pytest

from oddshawk_sdk import Rest, generate_hash
from oddshawk_sdk.hashing import generate_hash as hashing_generate_hash


def test_rest_constructs():
    client = Rest("user", "secret")
    assert client.user == "user"
    assert client.key == "secret"


def test_generate_hash_wire_shape(monkeypatch):
    ts = 1_714_000_000
    monkeypatch.setattr(time, "time", lambda: float(ts))
    expected = hashlib.sha256(f"test-password{ts}".encode("utf-8")).hexdigest() + format(ts, "x")
    assert hashing_generate_hash("test-password") == expected


def test_generate_hash_is_exported_and_deterministic():
    assert generate_hash is hashing_generate_hash
    assert generate_hash("k", 1_714_000_000) == generate_hash("k", 1_714_000_000)


def test_headers_include_user_and_hash(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 42.0)
    client = Rest("alice", "k")
    headers = client._headers()
    assert headers["X-OH-User"] == "alice"
    assert headers["X-OH-Hash"].endswith("2a")
    assert len(headers["X-OH-Hash"]) == 64 + 2
