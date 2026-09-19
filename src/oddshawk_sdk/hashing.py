"""Time-based hash for OddsHawk ``X-OH-Hash`` / ``X-OH-HASH`` headers."""

from __future__ import annotations

import hashlib
import time


def generate_hash(key: str, timestamp: int | None = None) -> str:
    """Build the auth hash wire value.

    Algorithm (matches the JS SDK and OddsHawk REST auth):

    1. Take unix seconds (UTC).
    2. SHA-256 hex digest of ``password + str(unix_seconds)`` (UTF-8).
    3. Append the unix seconds as lowercase hex (no ``0x`` prefix).

    The server reads the last 8 characters of the result as the hex timestamp.
    """
    if timestamp is None:
        timestamp = int(time.time())
    digest = hashlib.sha256(f"{key}{timestamp}".encode("utf-8")).hexdigest()
    hex_timestamp = format(timestamp, "x")
    return digest + hex_timestamp
