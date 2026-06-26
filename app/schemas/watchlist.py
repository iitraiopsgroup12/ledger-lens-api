from datetime import datetime
from typing import Literal

from pydantic import BaseModel

Frequency = Literal["daily", "weekly"]
WatchlistStatus = Literal["active", "paused"]


class WatchlistCreateRequest(BaseModel):
    symbol: str
    frequency: Frequency


class WatchlistEntry(BaseModel):
    id: str
    symbol: str
    frequency: Frequency
    status: WatchlistStatus


class WatchlistItem(BaseModel):
    symbol: str
    company_name: str
    frequency: Frequency
    last_update: datetime | None = None
    status: WatchlistStatus


class WatchlistUpdateRequest(BaseModel):
    frequency: Frequency


class WatchlistUpdateResponse(BaseModel):
    symbol: str
    frequency: Frequency
    updated: bool
