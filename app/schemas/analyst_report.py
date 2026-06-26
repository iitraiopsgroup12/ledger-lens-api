from datetime import date

from pydantic import BaseModel, Field


class AnalystReportUploadResponse(BaseModel):
    report_id: str
    status: str


class AnalystReport(BaseModel):
    report_id: str
    broker: str
    date: date
    sentiment_score: float | None = Field(default=None, ge=0, le=1)


class CompanySentiment(BaseModel):
    symbol: str
    buy: int
    hold: int
    sell: int
    score: float = Field(ge=0, le=1)
    reports_count: int
