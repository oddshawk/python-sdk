"""The OddsHawk REST client, with the query and URL helpers its reads are built from."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Optional
from urllib.parse import urlencode

import requests

from .hashing import generate_hash

DEFAULT_BASE_URL = "https://www.odds.software"


def build_query(from_now: Optional[bool] = None, params: Optional[Mapping[str, Any]] = None) -> str:
    """Booleans go on the wire lowercase, and a ``None`` value is omitted.

    :param from_now: Sent first as ``fromNow``; ``None`` sends none.
    :param params: Search keys to send.
    :return: The URL-encoded query string, empty when nothing is sent.
    """
    items: list[tuple[str, Any]] = []
    if from_now is not None:
        items.append(("fromNow", str(from_now).lower() if isinstance(from_now, bool) else from_now))
    if params:
        for key, value in params.items():
            if value is None:
                continue
            if isinstance(value, bool):
                items.append((key, str(value).lower()))
            else:
                items.append((key, value))
    return urlencode(items, doseq=True)


def build_url(path: str, query: str = "") -> str:
    """An empty query is left off.

    :param path: Request path, which the client expects to start with ``/``.
    :param query: Encoded query string, as ``build_query`` answers.
    :return: The path, with the query appended after ``?`` when there is one.
    """
    if not query:
        return path
    return f"{path}?{query}"


class Rest:
    """An authenticated client for one OddsHawk account: the odds catalog, and the resolution of a
    provider's own spelling to the canonical record."""

    def __init__(
        self,
        user: str,
        key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        session: Optional[requests.Session] = None,
        timeout: float = 15.0,
    ) -> None:
        """A client is bound to one account and one root URL.

        :param user: The account's user name, sent as ``X-OH-User``.
        :param key: The account's API key, which signs every request.
        :param base_url: Root the request paths are appended to; trailing slashes are dropped.
        :param session: HTTP session to send through, or a new one.
        :param timeout: Seconds a single request may take.
        """
        self.user = user
        self.key = key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = session or requests.Session()

    def _headers(self, timestamp: int | None = None) -> dict[str, str]:
        return {
            "X-OH-User": self.user,
            "X-OH-Hash": generate_hash(self.key, timestamp),
        }

    def _get(self, path: str, *, timestamp: int | None = None) -> Any:
        """Sends an authenticated GET and answers the body parsed as JSON.

        :param path: Request path appended to the base URL.
        :param timestamp: Unix second to sign for, or the current one.
        :return: The response body parsed as JSON.
        :raises requests.HTTPError: The API answered non-2xx; the message carries its status and body.
        :raises requests.RequestException: The request did not complete.
        :raises ValueError: The body was not JSON.
        """
        url = self.base_url + path
        response = self._session.get(
            url,
            headers=self._headers(timestamp),
            timeout=self.timeout,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise requests.HTTPError(
                f"OddsHawk API request failed ({response.status_code}): {response.text}",
                response=response,
            ) from exc
        return response.json()

    def authenticate(self) -> Any:
        return self._get("/authenticate")

    def version(self) -> Any:
        return self._get("/rest")

    def sports(self, from_now: bool = True) -> Any:
        """
        :param from_now: Sent as the ``fromNow`` parameter.
        """
        path = build_url("/rest/odds/sports", build_query(from_now=from_now))
        return self._get(path)

    def competitions(
        self,
        from_now: bool = True,
        search_params: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        """
        :param from_now: Sent as the ``fromNow`` parameter.
        :param search_params: The endpoint honours ``sport`` and ``provider``.
        :return: The competitions that match.
        """
        path = build_url(
            "/rest/odds/competitions",
            build_query(from_now=from_now, params=search_params),
        )
        return self._get(path)

    def events(
        self,
        from_now: bool = True,
        search_params: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        """
        :param from_now: Sent as the ``fromNow`` parameter.
        :param search_params: The endpoint honours ``sport``, ``provider``, ``competition`` and
            ``market``.
        :return: The events that match.
        """
        path = build_url(
            "/rest/odds/events",
            build_query(from_now=from_now, params=search_params),
        )
        return self._get(path)

    def markets(
        self,
        from_now: bool = True,
        search_params: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        """
        :param from_now: Sent as the ``fromNow`` parameter.
        :param search_params: The endpoint honours ``sport``, ``provider`` and ``competition``.
        :return: The markets that match.
        """
        path = build_url(
            "/rest/odds/markets",
            build_query(from_now=from_now, params=search_params),
        )
        return self._get(path)

    def providers(
        self,
        from_now: bool = True,
        search_params: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        """
        :param from_now: Sent as the ``fromNow`` parameter.
        :param search_params: The endpoint honours ``sport`` and ``competition``.
        :return: The providers that match.
        """
        path = build_url(
            "/rest/odds/providers",
            build_query(from_now=from_now, params=search_params),
        )
        return self._get(path)

    def odds(self, search_params: Optional[Mapping[str, Any]] = None) -> Any:
        """Searches the odds rows of ``GET /rest/odds``; every call is a fresh request.

        :param search_params: The endpoint honours ``eventTime``,
            ``eventName``, ``sport``, ``provider``, ``competition``, ``competitionName``,
            ``selectionStatus``, ``sortField``, ``sortDirection``, ``limit``, ``skip``, ``market``,
            ``fromNow`` and ``updatedBefore``.
        :return: The odds rows that match.
        """
        params: MutableMapping[str, Any] = dict(search_params or {})
        path = build_url("/rest/odds", build_query(params=params))
        return self._get(path)

    def _match(self, path: str, params: Mapping[str, Any]) -> Any:
        """Resolves through a ``/rest/match/*`` endpoint, answering ``False`` instead of raising.

        :param path: The match endpoint's path.
        :param params: Query parameters, as ``_match_params`` builds them.
        :return: The canonical match, or ``False`` on a request failure
            (``requests.RequestException``) or a body that is not JSON (``ValueError``).
        """
        try:
            return self._get(build_url(path, build_query(params=params)))
        except (requests.RequestException, ValueError):
            return False

    def _match_params(
        self,
        provider: str,
        name: str,
        time: int,
        sport: str,
        init: bool,
        event_name: Optional[str] = None,
    ) -> dict[str, Any]:
        """The query parameters a ``/rest/match/*`` read sends.

        :param provider: The provider the spelling came from.
        :param name: That provider's own spelling.
        :param time: Event start in unix seconds.
        :param sport: The sport the lookup is scoped to.
        :param init: Registers an unresolved name for curation when ``True``.
        :param event_name: The canonical event name, sent as ``event``; the selection lookup requires it.
        """
        params: dict[str, Any] = {
            "provider": provider,
            "name": name,
            "time": time,
            "sport": sport,
        }
        if event_name is not None:
            params["event"] = event_name
        params["init"] = init
        return params

    def match_event(
        self,
        provider: str,
        name: str,
        time: int,
        sport: str,
        init: bool = False,
    ) -> Any:
        """
        :param provider: The provider the spelling came from.
        :param name: The provider's spelling of the event.
        :param time: Event start in unix seconds.
        :param sport: The sport the event belongs to.
        :param init: Registers an unresolved name for curation when ``True``; that call still answers ``False``.
        :return: The canonical match, or ``False`` when nothing resolves or the request fails.
        """
        return self._match(
            "/rest/match/event",
            self._match_params(provider, name, time, sport, init),
        )

    def match_selection(
        self,
        provider: str,
        name: str,
        time: int,
        sport: str,
        event_name: str,
        init: bool = False,
    ) -> Any:
        """
        :param provider: The provider the spelling came from.
        :param name: The provider's spelling of the selection.
        :param time: Event start in unix seconds.
        :param sport: The sport the selection belongs to.
        :param event_name: The canonical event name, as ``/rest/match/event`` returned it.
        :param init: Registers an unresolved name for curation when ``True``.
        :return: The canonical match, or ``False`` when nothing resolves or the request fails.
        """
        return self._match(
            "/rest/match/selection",
            self._match_params(provider, name, time, sport, init, event_name=event_name),
        )

    def match_team(
        self,
        provider: str,
        name: str,
        time: int,
        sport: str,
        init: bool = False,
    ) -> Any:
        """
        :param provider: The provider the spelling came from.
        :param name: The provider's spelling of the team.
        :param time: Event start in unix seconds.
        :param sport: The sport the team belongs to.
        :param init: Registers an unresolved name for curation when ``True``.
        :return: The canonical match, or ``False`` when nothing resolves or the request fails.
        """
        return self._match(
            "/rest/match/team",
            self._match_params(provider, name, time, sport, init),
        )

    def match_competition(
        self,
        provider: str,
        name: str,
        time: int,
        sport: str,
        init: bool = False,
    ) -> Any:
        """
        :param provider: The provider the spelling came from.
        :param name: The provider's spelling of the competition.
        :param time: Event start in unix seconds.
        :param sport: The sport the competition belongs to.
        :param init: Registers an unresolved name for curation when ``True``.
        :return: The canonical match, or ``False`` when nothing resolves or the request fails.
        """
        return self._match(
            "/rest/match/competition",
            self._match_params(provider, name, time, sport, init),
        )
