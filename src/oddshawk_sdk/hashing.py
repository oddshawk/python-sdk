"""The signature the OddsHawk API checks, carried in the ``X-OH-Hash`` request header."""

from __future__ import annotations

import hashlib
import time


def generate_hash(key: str, timestamp: int | None = None) -> str:
    """Answers the wire value the API accepts: the SHA-256 hex digest of the key followed by the
    second, then that second in lowercase hex.

    :param key: The account's API key, the only secret the value is computed from.
    :param timestamp: Unix second in UTC to name, or the current one.
    :return: The value carried in the request's signature header.
    """
    if timestamp is None:
        timestamp = int(time.time())
    digest = hashlib.sha256(f"{key}{timestamp}".encode("utf-8")).hexdigest()
    hex_timestamp = format(timestamp, "x")
    return digest + hex_timestamp
