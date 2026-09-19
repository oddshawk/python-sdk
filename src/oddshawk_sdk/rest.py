"""REST client for the OddsHawk REST API."""

from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Optional
from urllib.parse import urlencode

import requests

from .hashing import generate_hash

DEFAULT_BASE_URL = "https://www.odds.software"


def build_query(from_now: Optional[bool] = None, params: Optional[Mapping[str, Any]] = None) -> str:
    """Build a query string for catalog endpoints.

    ``from_now`` maps to the ``fromNow`` query param when not ``None``.
    Other params are URL-encoded; ``None`` values are omitted.
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
    """Join a path with an optional query string (path must start with ``/``)."""
    if not query:
        return path
    return f"{path}?{query}"


class Rest:
    """HMAC-authenticated client for the OddsHawk REST API.

    Catalog methods mirror the OpenAPI public surface used by the docs quickstart:
    ``authenticate``, ``version``, ``sports``, ``competitions``, ``events``,
    ``markets``, ``providers``, and ``odds``.

    The ``match_*`` methods wrap the ``/rest/match/*`` endpoints, documented in the OpenAPI
    ``Matching`` section. Like every other ``/rest`` endpoint, they are available to any
    authenticated account. They return ``False`` on failure, mirroring the JS SDK.

    WebSocket streaming is not included in this package yet (REST-first).
    """

    def __init__(
        self,
        user: str,
        key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        session: Optional[requests.Session] = None,
        timeout: float = 15.0,
    ) -> None:
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
        """``GET /authenticate`` — validate credentials (and establish session cookie if used)."""
        return self._get("/authenticate")

    def version(self) -> Any:
        """``GET /rest`` — public API version payload."""
        return self._get("/rest")

    def sports(self, from_now: bool = True) -> Any:
        """``GET /rest/odds/sports`` — distinct sport names."""
        path = build_url("/rest/odds/sports", build_query(from_now=from_now))
        return self._get(path)

    def competitions(
        self,
        from_now: bool = True,
        search_params: Optional[Mapping[str, Any]] = None,
    ) -> Any:
        """``GET /rest/odds/competitions``.

        ``search_params`` may include ``sport`` and ``provider``.
        Specifying ``provider`` bypasses cache and may be slower.
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
        """``GET /rest/odds/events``.

        ``search_params`` may include ``sport``, ``provider``, ``competition``, and ``market``.
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
        """``GET /rest/odds/markets``.

        ``search_params`` may include ``sport``, ``provider``, and ``competition``.
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
        """``GET /rest/odds/providers``.

        ``search_params`` may include ``sport`` and ``competition``.
        """
        path = build_url(
            "/rest/odds/providers",
            build_query(from_now=from_now, params=search_params),
        )
        return self._get(path)

    def odds(self, search_params: Optional[Mapping[str, Any]] = None) -> Any:
        """``GET /rest/odds`` — search odds rows.

        Common params: ``eventTime``, ``eventName``, ``sport``, ``provider``,
        ``competition``, ``competitionName``, ``selectionStatus``, ``sortField``,
        ``sortDirection``, ``limit``, ``skip``, ``market``, ``fromNow``, ``eventId``,
        ``updatedBefore``. Never cached. Limits above 200 require a specific event
        or ``sport``+``provider`` pair.
        """
        params: MutableMapping[str, Any] = dict(search_params or {})
        path = build_url("/rest/odds", build_query(params=params))
        return self._get(path)

    def _match(self, path: str, params: Mapping[str, Any]) -> Any:
        """GET a ``/rest/match/*`` endpoint, mirroring the JS SDK contract.

        Match helpers return ``False`` on any failure (400/403/404/transport) instead of raising,
        matching ``@oddshawk/oddshawk-sdk``.
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
        """``GET /rest/match/event`` — resolve a provider event name to a canonical event.

        Available to any authenticated account, like the rest of ``/rest``. Returns the canonical
        match payload, or ``False`` when the API has no match (or on failure). ``init=True``
        registers an unresolved name for curation — the call that registers it still returns
        ``False``.
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
        """``GET /rest/match/selection`` — resolve a provider selection name to a canonical selection.

        Available to any authenticated account, like the rest of ``/rest``. ``event_name`` is
        required (it is used by the Betfair Exchange lookup). Returns the canonical match payload,
        or ``False`` when the API has no match (or on failure).
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
        """``GET /rest/match/team`` — resolve a provider team name to a canonical team.

        Available to any authenticated account, like the rest of ``/rest``. Returns the canonical
        match payload, or ``False`` when the API has no match (or on failure).
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
        """``GET /rest/match/competition`` — resolve a provider competition name to a canonical one.

        Available to any authenticated account, like the rest of ``/rest``. Returns the canonical
        match payload, or ``False`` when the API has no match (or on failure).
        """
        return self._match(
            "/rest/match/competition",
            self._match_params(provider, name, time, sport, init),
        )
