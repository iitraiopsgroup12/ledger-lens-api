"""Analyst Report module business logic.

Analyst reports are manually uploaded (no automated MCP ingestion), then
processed through the same RAG pipeline and rolled up into a per-company
buy/hold/sell sentiment score.
"""

from abc import ABC, abstractmethod
from datetime import date
from uuid import uuid4

from app.schemas.analyst_report import AnalystReport, AnalystReportUploadResponse, CompanySentiment


class AnalystReportService(ABC):
    @abstractmethod
    def upload(self, company: str, broker: str, report_date: date, file_bytes: bytes) -> AnalystReportUploadResponse: ...

    @abstractmethod
    def list_for_company(self, symbol: str) -> list[AnalystReport]: ...

    @abstractmethod
    def get_sentiment(self, symbol: str) -> CompanySentiment: ...


class InMemoryAnalystReportService(AnalystReportService):
    """Placeholder implementation. TODO: validate PDF, store in S3, and trigger RAG + sentiment scoring."""

    def __init__(self) -> None:
        self._reports: dict[str, list[dict]] = {}

    def upload(self, company: str, broker: str, report_date: date, file_bytes: bytes) -> AnalystReportUploadResponse:
        symbol = company.upper()
        report_id = str(uuid4())
        self._reports.setdefault(symbol, []).append(
            {"report_id": report_id, "broker": broker, "date": report_date, "sentiment_score": None}
        )
        # TODO: enqueue async RAG processing + sentiment scoring for the uploaded PDF.
        return AnalystReportUploadResponse(report_id=report_id, status="processing")

    def list_for_company(self, symbol: str) -> list[AnalystReport]:
        symbol = symbol.upper()
        return [AnalystReport(**report) for report in self._reports.get(symbol, [])]

    def get_sentiment(self, symbol: str) -> CompanySentiment:
        symbol = symbol.upper()
        reports = self._reports.get(symbol, [])
        # TODO: compute a real weighted buy/hold/sell aggregate from sentiment_score values.
        return CompanySentiment(symbol=symbol, buy=0, hold=0, sell=0, score=0.5, reports_count=len(reports))
