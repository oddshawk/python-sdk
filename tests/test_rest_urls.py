"""Tests for catalog URL / query building and request headers."""

from unittest.mock import MagicMock

import pytest
import requests

from oddshawk_sdk.rest import Rest, build_query, build_url


def test_build_query_from_now_lowercase_bool():
    assert build_query(from_now=True) == "fromNow=true"
    assert build_query(from_now=False) == "fromNow=false"


def test_build_query_merges_search_params():
    q = build_query(from_now=True, params={"sport": "Football", "provider": "Bet365"})
    assert q == "fromNow=true&sport=Football&provider=Bet365"


def test_build_query_omits_none_and_encodes_spaces():
    q = build_query(params={"sport": "Horse Racing", "market": None})
    assert q == "sport=Horse+Racing"


def test_build_query_empty():
    assert build_query() == ""
    assert build_query(params={}) == ""


def test_build_url_with_and_without_query():
    assert build_url("/rest/odds/sports") == "/rest/odds/sports"
    assert build_url("/rest/odds/sports", "fromNow=true") == "/rest/odds/sports?fromNow=true"


@pytest.mark.parametrize(
    "method,kwargs,expected_path",
    [
        ("sports", {"from_now": True}, "/rest/odds/sports?fromNow=true"),
        ("sports", {"from_now": False}, "/rest/odds/sports?fromNow=false"),
        (
            "competitions",
            {"from_now": True, "search_params": {"sport": "Football"}},
            "/rest/odds/competitions?fromNow=true&sport=Football",
        ),
        (
            "events",
            {"from_now": True, "search_params": {"sport": "Football", "market": "Match Odds"}},
            "/rest/odds/events?fromNow=true&sport=Football&market=Match+Odds",
        ),
        (
            "markets",
            {"from_now": True, "search_params": {"sport": "Football"}},
            "/rest/odds/markets?fromNow=true&sport=Football",
        ),
        (
            "providers",
            {"from_now": True, "search_params": {"sport": "Football"}},
            "/rest/odds/providers?fromNow=true&sport=Football",
        ),
        (
            "odds",
            {"search_params": {"sport": "Football", "limit": 10}},
            "/rest/odds?sport=Football&limit=10",
        ),
        (
            "match_event",
            {"provider": "Bet365", "name": "Arsenal v Chelsea", "time": 12345, "sport": "Football"},
            "/rest/match/event?provider=Bet365&name=Arsenal+v+Chelsea&time=12345&sport=Football&init=false",
        ),
        (
            "match_event",
            {
                "provider": "Bet365",
                "name": "Arsenal",
                "time": 12345,
                "sport": "Football",
                "init": True,
            },
            "/rest/match/event?provider=Bet365&name=Arsenal&time=12345&sport=Football&init=true",
        ),
        (
            "match_selection",
            {
                "provider": "Bet365",
                "name": "Over 2.5",
                "time": 12345,
                "sport": "Football",
                "event_name": "Arsenal v Chelsea",
            },
            "/rest/match/selection?provider=Bet365&name=Over+2.5&time=12345&sport=Football"
            "&event=Arsenal+v+Chelsea&init=false",
        ),
        (
            "match_team",
            {"provider": "Bet365", "name": "Arsenal", "time": 12345, "sport": "Football"},
            "/rest/match/team?provider=Bet365&name=Arsenal&time=12345&sport=Football&init=false",
        ),
        (
            "match_competition",
            {"provider": "Bet365", "name": "Premier League", "time": 12345, "sport": "Football"},
            "/rest/match/competition?provider=Bet365&name=Premier+League&time=12345&sport=Football"
            "&init=false",
        ),
        ("authenticate", {}, "/authenticate"),
        ("version", {}, "/rest"),
    ],
)
def test_rest_methods_build_expected_paths(method, kwargs, expected_path):
    session = MagicMock()
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"ok": True}
    response.raise_for_status = MagicMock()
    session.get.return_value = response

    client = Rest("user@example.com", "secret", session=session, base_url="https://www.odds.software")
    getattr(client, method)(**kwargs)

    session.get.assert_called_once()
    args, kwargs_call = session.get.call_args
    assert args[0] == "https://www.odds.software" + expected_path
    headers = kwargs_call["headers"]
    assert headers["X-OH-User"] == "user@example.com"
    assert "X-OH-Hash" in headers
    assert len(headers["X-OH-Hash"]) > 64


def test_rest_headers_use_fixed_timestamp(monkeypatch):
    import oddshawk_sdk.hashing as hashing

    monkeypatch.setattr(hashing.time, "time", lambda: 1_700_000_000)

    session = MagicMock()
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = []
    response.raise_for_status = MagicMock()
    session.get.return_value = response

    client = Rest("u", "k", session=session)
    client.sports()

    headers = session.get.call_args.kwargs["headers"]
    from oddshawk_sdk import generate_hash

    assert headers["X-OH-Hash"] == generate_hash("k", timestamp=1_700_000_000)


def _response(payload):
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = payload
    response.raise_for_status = MagicMock()
    return response


def test_match_helpers_return_payload_on_success():
    session = MagicMock()
    session.get.return_value = _response({"_id": "e1", "string": "Arsenal v Chelsea"})
    client = Rest("u", "k", session=session)

    result = client.match_event("Bet365", "Arsenal v Chelsea", 12345, "Football")

    assert result == {"_id": "e1", "string": "Arsenal v Chelsea"}
    assert session.get.call_args.args[0] == (
        "https://www.odds.software/rest/match/event"
        "?provider=Bet365&name=Arsenal+v+Chelsea&time=12345&sport=Football&init=false"
    )


def test_match_selection_sends_event_param():
    session = MagicMock()
    session.get.return_value = _response({"_id": "s1"})
    client = Rest("u", "k", session=session)

    client.match_selection("Bet365", "Over 2.5", 12345, "Football", "Arsenal v Chelsea", init=True)

    assert session.get.call_args.args[0] == (
        "https://www.odds.software/rest/match/selection"
        "?provider=Bet365&name=Over+2.5&time=12345&sport=Football"
        "&event=Arsenal+v+Chelsea&init=true"
    )


def test_match_helpers_return_false_on_http_error():
    session = MagicMock()
    error_response = MagicMock()
    error_response.status_code = 404
    error_response.text = '{"error":"Not found"}'
    error_response.raise_for_status.side_effect = requests.HTTPError(response=error_response)
    session.get.return_value = error_response
    client = Rest("u", "k", session=session)

    assert client.match_event("Bet365", "nope", 1, "Football") is False
    assert client.match_selection("Bet365", "nope", 1, "Football", "x") is False
    assert client.match_team("Bet365", "nope", 1, "Football") is False
    assert client.match_competition("Bet365", "nope", 1, "Football") is False


def test_match_helpers_return_false_on_transport_error():
    session = MagicMock()
    session.get.side_effect = requests.ConnectionError("boom")
    client = Rest("u", "k", session=session)

    assert client.match_team("Bet365", "Arsenal", 12345, "Football") is False


def test_match_helpers_return_false_on_invalid_json():
    session = MagicMock()
    error_response = _response(None)
    error_response.json.side_effect = ValueError("No JSON")
    session.get.return_value = error_response
    client = Rest("u", "k", session=session)

    assert client.match_competition("Bet365", "Premier League", 12345, "Football") is False
