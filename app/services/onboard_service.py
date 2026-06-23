"""Company onboarding orchestration.

`/onboard` on ledger-lens-sync (see docs/servers/ledger-lens-sync.json) kicks
off discovery/sync of a company's filings; results land in the user's
watchlist once that sync completes. The caller doesn't wait on it.
"""

import logging
from abc import ABC, abstractmethod

from app.clients.sync_client import SyncServiceClient

logger = logging.getLogger(__name__)


class OnboardService(ABC):
    @abstractmethod
    def start_onboarding(self, symbol: str, user_id: int) -> None: ...


class SyncOnboardService(OnboardService):
    def __init__(self, sync_client: SyncServiceClient) -> None:
        self._sync_client = sync_client

    def start_onboarding(self, symbol: str, user_id: int) -> None:
        try:
            self._sync_client.onboard_company(symbol, user_id)
        except Exception:
            logger.exception("Onboarding failed for symbol=%s user_id=%s", symbol, user_id)