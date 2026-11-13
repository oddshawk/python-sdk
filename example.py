"""A stand-in smoke program: walks the catalog for the account the environment names."""

import os

from oddshawk_sdk import Rest


def credentials_from_env() -> tuple[str, str]:
    """
    :return: The user name and key, in that order.
    :raises SystemExit: ``OH_USER`` or ``OH_SECRET`` is unset or empty; the message names both variables.
    """
    user = os.environ.get("OH_USER")
    secret = os.environ.get("OH_SECRET")
    if not user or not secret:
        raise SystemExit("OH_USER and OH_SECRET must both be set")
    return user, secret


def main():
    user, secret = credentials_from_env()
    client = Rest(user, secret)
    sports = client.sports()
    for sport in sports:
        print(sport)
        print("Available Markets:")
        markets = client.markets(True, {"sport": sport})
        print(markets)
        competitions = client.competitions(True, {"sport": sport})
        if len(competitions) > 0:
            print(competitions[0]["name"])
            events = client.events(
                True, {"sport": sport, "competition": competitions[0]["id"]}
            )
            if len(events) > 0:
                print(events[0]["name"])
                print(events[0]["time"])
                odds = client.odds(
                    {
                        "fromNow": True,
                        "sport": sport,
                        "eventName": events[0]["name"],
                        "eventTime": events[0]["time"],
                        "limit": 1,
                    }
                )
                print(odds)


if __name__ == "__main__":
    main()
