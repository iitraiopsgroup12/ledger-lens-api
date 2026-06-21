"""Dashboard module business logic. Aggregates watchlist, ingestion, and activity stats for one summary call."""

from abc import ABC, abstractmethod

from app.schemas.dashboard import DashboardResponse


class DashboardService(ABC):
    @abstractmethod
    def get_summary(self, user_id: str) -> DashboardResponse: ...


class InMemoryDashboardService(DashboardService):
    """Placeholder implementation. TODO: aggregate real counts from watchlists/documents/update_logs."""

    def get_summary(self, user_id: str) -> DashboardResponse:
        return DashboardResponse(watchlist_count=0, new_reports=0, pending_processing=0, recent_updates=[])
