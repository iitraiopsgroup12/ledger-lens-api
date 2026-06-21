"""Watchlist module business logic.

Per docs/API_Documentation.docx Flow 1 & Flow 2: a watchlist entry
(user_id, company_id, frequency, status) drives the hourly scheduler,
which compares last_checked + frequency against now().
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from uuid import uuid4

from app.schemas.watchlist import (
    Frequency,
    WatchlistEntry,
    WatchlistItem,
    WatchlistUpdateResponse,
)
from app.services.exceptions import ConflictError, NotFoundError


class WatchlistService(ABC):
    @abstractmethod
    def add(self, user_id: str, symbol: str, frequency: Frequency) -> WatchlistEntry: ...

    @abstractmethod
    def list_for_user(self, user_id: str) -> list[WatchlistItem]: ...

    @abstractmethod
    def update_frequency(self, user_id: str, symbol: str, frequency: Frequency) -> WatchlistUpdateResponse: ...

    @abstractmethod
    def remove(self, user_id: str, symbol: str) -> None: ...


class InMemoryWatchlistService(WatchlistService):
    """Placeholder implementation. TODO: back with the Postgres `watchlists` table."""

    def __init__(self) -> None:
        self._entries: dict[tuple[str, str], dict] = {}

    def add(self, user_id: str, symbol: str, frequency: Frequency) -> WatchlistEntry:
        symbol = symbol.upper()
        key = (user_id, symbol)
        if key in self._entries:
            raise ConflictError(f"'{symbol}' is already in the watchlist")
        entry = {
            "id": str(uuid4()),
            "symbol": symbol,
            "frequency": frequency,
            "status": "active",
            "last_checked": None,
        }
        self._entries[key] = entry
        return WatchlistEntry(id=entry["id"], symbol=symbol, frequency=frequency, status="active")

    def list_for_user(self, user_id: str) -> list[WatchlistItem]:
        return [
            WatchlistItem(
                symbol=entry["symbol"],
                company_name=entry["symbol"],
                frequency=entry["frequency"],
                last_update=entry["last_checked"],
                status=entry["status"],
            )
            for (uid, _symbol), entry in self._entries.items()
            if uid == user_id
        ]

    def update_frequency(self, user_id: str, symbol: str, frequency: Frequency) -> WatchlistUpdateResponse:
        symbol = symbol.upper()
        key = (user_id, symbol)
        entry = self._entries.get(key)
        if entry is None:
            raise NotFoundError(f"'{symbol}' is not in the watchlist")
        entry["frequency"] = frequency
        return WatchlistUpdateResponse(symbol=symbol, frequency=frequency, updated=True)

    def remove(self, user_id: str, symbol: str) -> None:
        symbol = symbol.upper()
        key = (user_id, symbol)
        if key not in self._entries:
            raise NotFoundError(f"'{symbol}' is not in the watchlist")
        del self._entries[key]
