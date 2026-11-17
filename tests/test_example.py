"""Tests for the credential resolver and the catalog walk the smoke script performs."""

import importlib.util
import runpy
from pathlib import Path

import pytest

import oddshawk_sdk

EXAMPLE_PATH = Path(__file__).resolve().parents[1] / "example.py"
MISSING_PAIR_MESSAGE = "OH_USER and OH_SECRET must both be set"
MARKETS_LABEL = "Available Markets:"
SOCCER = "soccer"
TENNIS = "tennis"
MARKETS = [{"name": "Match Winner"}]
COMPETITION = {"id": 11, "name": "English Premier League"}
EVENT = {"name": "Arsenal v Chelsea", "time": 1_714_000_000}
ODDS = [{"selection": "Arsenal", "price": 2.1}]


def load_example():
    spec = importlib.util.spec_from_file_location("example", EXAMPLE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def example():
    return load_example()


@pytest.fixture()
def configured_pair(monkeypatch):
    monkeypatch.setenv("OH_USER", "a-user")
    monkeypatch.setenv("OH_SECRET", "a-secret")


def stub_client(monkeypatch, target, *, sports=(), competitions=(), events=(), odds=()):
    """Point ``target``'s ``Rest`` at a stub that records each read and answers the seeded rows."""
    instances = []

    class StubRest:
        """The client surface ``main`` reads: each call is recorded, each answer is a seeded row."""

        def __init__(self, user, key):
            self.user = user
            self.key = key
            self.calls = []
            instances.append(self)

        def sports(self):
            self.calls.append(("sports",))
            return list(sports)

        def markets(self, from_now, search_params):
            self.calls.append(("markets", from_now, dict(search_params)))
            return list(MARKETS)

        def competitions(self, from_now, search_params):
            self.calls.append(("competitions", from_now, dict(search_params)))
            return list(competitions)

        def events(self, from_now, search_params):
            self.calls.append(("events", from_now, dict(search_params)))
            return list(events)

        def odds(self, search_params):
            self.calls.append(("odds", dict(search_params)))
            return list(odds)

    monkeypatch.setattr(target, "Rest", StubRest)
    return instances


def run_main(monkeypatch, target, **rows):
    """Run ``target``'s ``main`` against a stubbed ``Rest``, and answer the stub it built."""
    instances = stub_client(monkeypatch, target, **rows)
    target.main()
    (instance,) = instances
    return instance


def test_credentials_from_env_returns_the_configured_pair(monkeypatch, example):
    monkeypatch.setenv("OH_USER", "a-user")
    monkeypatch.setenv("OH_SECRET", "a-secret")

    assert example.credentials_from_env() == ("a-user", "a-secret")


@pytest.mark.parametrize(
    "environment",
    [
        {},
        {"OH_USER": "a-user"},
        {"OH_SECRET": "a-secret"},
        {"OH_USER": "", "OH_SECRET": "a-secret"},
        {"OH_USER": "a-user", "OH_SECRET": ""},
        {"OH_USER": "", "OH_SECRET": ""},
    ],
)
def test_credentials_from_env_refuses_an_unset_or_empty_pair(
    environment, monkeypatch, example
):
    monkeypatch.delenv("OH_USER", raising=False)
    monkeypatch.delenv("OH_SECRET", raising=False)
    for name, value in environment.items():
        monkeypatch.setenv(name, value)

    with pytest.raises(SystemExit) as raised:
        example.credentials_from_env()

    assert str(raised.value) == MISSING_PAIR_MESSAGE
    assert "OH_USER" in str(raised.value)
    assert "OH_SECRET" in str(raised.value)


def test_main_builds_the_client_from_the_configured_pair(
    configured_pair, example, monkeypatch
):
    client = run_main(monkeypatch, example, sports=[SOCCER])

    assert (client.user, client.key) == ("a-user", "a-secret")


def test_main_reads_the_markets_of_every_sport(configured_pair, example, monkeypatch):
    client = run_main(monkeypatch, example, sports=[SOCCER, TENNIS])

    markets_calls = [call for call in client.calls if call[0] == "markets"]
    assert markets_calls == [
        ("markets", True, {"sport": SOCCER}),
        ("markets", True, {"sport": TENNIS}),
    ]


def test_main_reports_a_sport_with_the_markets_label_and_its_markets(
    configured_pair, example, monkeypatch, capsys
):
    run_main(monkeypatch, example, sports=[SOCCER])

    printed = capsys.readouterr().out.splitlines()
    assert SOCCER in printed
    assert MARKETS_LABEL in printed
    assert repr(MARKETS) in printed


def test_main_reads_the_competitions_of_the_sport(
    configured_pair, example, monkeypatch
):
    client = run_main(monkeypatch, example, sports=[SOCCER], competitions=[COMPETITION])

    assert [call for call in client.calls if call[0] == "competitions"] == [
        ("competitions", True, {"sport": SOCCER}),
    ]


def test_main_reports_the_first_competition_of_the_sport(
    configured_pair, example, monkeypatch, capsys
):
    run_main(monkeypatch, example, sports=[SOCCER], competitions=[COMPETITION])

    assert COMPETITION["name"] in capsys.readouterr().out.splitlines()


def test_main_reads_the_events_of_the_first_competition(
    configured_pair, example, monkeypatch
):
    client = run_main(
        monkeypatch,
        example,
        sports=[SOCCER],
        competitions=[COMPETITION],
        events=[EVENT],
    )

    assert [call for call in client.calls if call[0] == "events"] == [
        ("events", True, {"sport": SOCCER, "competition": COMPETITION["id"]}),
    ]


def test_main_reads_one_odds_record_for_the_first_event(
    configured_pair, example, monkeypatch
):
    client = run_main(
        monkeypatch,
        example,
        sports=[SOCCER],
        competitions=[COMPETITION],
        events=[EVENT],
        odds=ODDS,
    )

    assert [call for call in client.calls if call[0] == "odds"] == [
        (
            "odds",
            {
                "fromNow": True,
                "sport": SOCCER,
                "eventName": EVENT["name"],
                "eventTime": EVENT["time"],
                "limit": 1,
            },
        ),
    ]


def test_main_reports_the_first_event_with_its_time_and_the_odds(
    configured_pair, example, monkeypatch, capsys
):
    run_main(
        monkeypatch,
        example,
        sports=[SOCCER],
        competitions=[COMPETITION],
        events=[EVENT],
        odds=ODDS,
    )

    printed = capsys.readouterr().out.splitlines()
    assert EVENT["name"] in printed
    assert str(EVENT["time"]) in printed
    assert repr(ODDS) in printed


def test_main_reads_nothing_further_when_the_sport_has_no_competitions(
    configured_pair, example, monkeypatch
):
    client = run_main(monkeypatch, example, sports=[SOCCER])

    read = [call[0] for call in client.calls]
    assert "events" not in read
    assert "odds" not in read


def test_main_reads_nothing_further_when_the_competition_has_no_events(
    configured_pair, example, monkeypatch
):
    client = run_main(monkeypatch, example, sports=[SOCCER], competitions=[COMPETITION])

    assert "odds" not in [call[0] for call in client.calls]


def test_main_prints_nothing_when_the_catalog_holds_no_sports(
    configured_pair, example, monkeypatch, capsys
):
    run_main(monkeypatch, example)

    assert capsys.readouterr().out == ""


def test_the_main_guard_runs_the_walk_when_the_script_is_executed(
    configured_pair, monkeypatch
):
    instances = stub_client(monkeypatch, oddshawk_sdk, sports=[SOCCER])

    runpy.run_path(str(EXAMPLE_PATH), run_name="__main__")

    assert instances[0].calls[0] == ("sports",)
