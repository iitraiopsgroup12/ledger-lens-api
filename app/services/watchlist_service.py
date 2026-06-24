"""Watchlist module business logic.

Per docs/API_Documentation.docx Flow 1 & Flow 2: a watchlist entry
(user_id, company_id, frequency, status) drives the hourly scheduler,
which compares last_checked + frequency against now().

Entries are *added* through the onboarding flow (`/onboard` -> ledger-lens-sync),
so this service only reads the current watchlist for display.
"""

from abc import ABC, abstractmethod

from app.clients.sync_client import SyncServiceClient
from app.schemas.watchlist import WatchlistItem


class WatchlistService(ABC):
    @abstractmethod
    def list_for_user(self, user_id: str) -> list[WatchlistItem]: ...


class SyncWatchlistService(WatchlistService):
    """Reads watchlist entries from ledger-lens-sync and resolves company names."""

    def __init__(self, sync_client: SyncServiceClient) -> None:
        self._sync_client = sync_client

    def list_for_user(self, user_id: str) -> list[WatchlistItem]:
        uid = int(user_id)
        entries = [w for w in self._sync_client.list_watchlists(limit=500) if w.get("user_id") == uid]
        if not entries:
            return []
        companies = {c["id"]: c for c in self._sync_client.list_companies(limit=500)}
        return [
            WatchlistItem(
                symbol=(company := companies.get(entry["company_id"], {})).get("symbol", ""),
                company_name=company.get("company_name") or company.get("symbol", ""),
                frequency=entry["frequency"],
                last_update=entry.get("last_checked"),
                status=entry["status"],
            )
            for entry in entries
        ]