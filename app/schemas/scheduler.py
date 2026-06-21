from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class SchedulerRunResponse(BaseModel):
    status: str
    companies_checked: int
    new_documents: int


class SchedulerStatus(BaseModel):
    last_run: datetime | None
    status: Literal["idle", "running"]
    next_run: datetime | None
