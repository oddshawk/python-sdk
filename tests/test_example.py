"""Tests for the credential resolver the smoke script uses."""

import importlib.util
from pathlib import Path

import pytest

EXAMPLE_PATH = Path(__file__).resolve().parents[1] / "example.py"
MISSING_PAIR_MESSAGE = "OH_USER and OH_SECRET must both be set"


def load_example():
    spec = importlib.util.spec_from_file_location("example", EXAMPLE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def example():
    return load_example()


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
