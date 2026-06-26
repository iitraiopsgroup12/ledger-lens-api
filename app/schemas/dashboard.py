from datetime import datetime

from pydantic import BaseModel


class DashboardUpdate(BaseModel):
    company: str
    event: str
    timestamp: datetime


class DashboardResponse(BaseModel):
    watchlist_count: int
    new_reports: int
    pending_processing: int
    recent_updates: list[DashboardUpdate]
