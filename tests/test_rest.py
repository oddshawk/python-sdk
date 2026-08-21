"""Smoke tests for OddsHawk Python SDK hash / Rest surface (cn-123)."""

import hashlib
import time

from oddshawk_sdk import Rest


def test_rest_constructs():
    client = Rest("user", "secret")
    assert client.user == "user"
    assert client.key == "secret"


def test_generate_hash_wire_shape(monkeypatch):
    ts = 1_714_000_000
    monkeypatch.setattr(time, "time", lambda: float(ts))
    client = Rest("u", "test-password")
    expected = hashlib.sha256(f"test-password{ts}".encode("utf-8")).hexdigest() + format(ts, "x")
    assert client._Rest__generate_hash() == expected


def test_get_headers_include_user_and_hash(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 42.0)
    client = Rest("alice", "k")
    headers = client._Rest__get_headers()
    assert headers["X-OH-User"] == "alice"
    assert headers["X-OH-Hash"].endswith("2a")
    assert len(headers["X-OH-Hash"]) == 64 + 2
