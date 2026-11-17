"""Tests for the REST client and its request signing."""

import hashlib
import time
from unittest.mock import MagicMock

import pytest
import requests

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


def _json_response(payload):
    """An HTTP session answer the client reads: a 2xx with ``payload`` as its parsed body."""
    response = MagicMock()
    response.status_code = 200
    response.text = ""
    response.json.return_value = payload
    response.raise_for_status = MagicMock()
    return response


def test_client_builds_a_session_when_none_is_given():
    assert isinstance(Rest("user", "secret")._session, requests.Session)


def test_client_keeps_the_session_it_is_given():
    session = MagicMock()

    assert Rest("user", "secret", session=session)._session is session


def test_client_drops_the_trailing_slash_of_its_base_url():
    session = MagicMock()
    session.get.return_value = _json_response({})
    client = Rest("user", "key", base_url="https://www.odds.software/", session=session)

    client.version()

    assert client.base_url == "https://www.odds.software"
    assert session.get.call_args.args[0] == "https://www.odds.software/rest"


def test_client_sends_its_timeout_and_lets_a_caller_override_it():
    default_session = MagicMock()
    default_session.get.return_value = _json_response({})
    custom_session = MagicMock()
    custom_session.get.return_value = _json_response({})

    Rest("user", "key", session=default_session).version()
    Rest("user", "key", session=custom_session, timeout=2.5).version()

    assert default_session.get.call_args.kwargs["timeout"] == 15.0
    assert custom_session.get.call_args.kwargs["timeout"] == 2.5


def test_a_read_answers_the_parsed_body():
    session = MagicMock()
    session.get.return_value = _json_response([{"sport": "soccer"}])

    assert Rest("user", "key", session=session).sports() == [{"sport": "soccer"}]


def test_an_explicit_timestamp_signs_the_request():
    session = MagicMock()
    session.get.return_value = _json_response({})

    Rest("user", "key", session=session)._get("/rest", timestamp=1_714_000_000)

    headers = session.get.call_args.kwargs["headers"]
    assert headers["X-OH-Hash"] == generate_hash("key", 1_714_000_000)


def test_odds_without_search_params_sends_no_query_string():
    session = MagicMock()
    session.get.return_value = _json_response([])

    Rest("user", "key", session=session).odds()

    assert session.get.call_args.args[0] == "https://www.odds.software/rest/odds"


def test_a_non_2xx_answer_raises_an_error_carrying_the_status_and_the_body():
    session = MagicMock()
    response = _json_response(None)
    response.status_code = 403
    response.text = '{"error":"coverage_not_entitled"}'
    response.raise_for_status.side_effect = requests.HTTPError("403 Client Error")
    session.get.return_value = response

    with pytest.raises(requests.HTTPError) as raised:
        Rest("user", "key", session=session).version()

    assert str(raised.value) == (
        'OddsHawk API request failed (403): {"error":"coverage_not_entitled"}'
    )
    assert raised.value.response is response
    assert isinstance(raised.value.__cause__, requests.HTTPError)
