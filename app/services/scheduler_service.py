"""Scheduler module business logic.

Per docs/API_Documentation.docx Flow 2: runs hourly via APScheduler/Celery
Beat, querying `watchlists` for entries where last_checked + frequency <
now(), and logging each run's outcome to `update_logs`.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone

from app.schemas.scheduler import SchedulerRunResponse, SchedulerStatus


class SchedulerService(ABC):
    @abstractmethod
    def trigger_run(self) -> SchedulerRunResponse: ...

    @abstractmethod
    def get_status(self) -> SchedulerStatus: ...


class InMemorySchedulerService(SchedulerService):
    """Placeholder implementation. TODO: wire to the real APScheduler/Celery Beat hourly job."""

    def __init__(self) -> None:
        self._last_run: datetime | None = None

    def trigger_run(self) -> SchedulerRunResponse:
        self._last_run = datetime.now(timezone.utc)
        # TODO: iterate due watchlist entries, call MCP, ingest new documents, write update_logs.
        return SchedulerRunResponse(status="triggered", companies_checked=0, new_documents=0)

    def get_status(self) -> SchedulerStatus:
        return SchedulerStatus(last_run=self._last_run, status="idle", next_run=None)
