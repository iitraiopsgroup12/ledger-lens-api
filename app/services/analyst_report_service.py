"""Analyst Report module business logic.

Analyst reports are manually uploaded (no automated MCP ingestion), stored in
ledger-lens-sync's `/analyst-reports` resource (see
docs/servers/ledger-lens-sync.json), processed through the RAG pipeline, and
rolled up into a per-company buy/hold/sell sentiment score.
"""

from abc import ABC, abstractmethod
from datetime import date

from app.clients.sync_client import JsonObject, SyncServiceClient
from app.schemas.analyst_report import AnalystReport, AnalystReportUploadResponse, CompanySentiment


class AnalystReportService(ABC):
    @abstractmethod
    def upload(
        self,
        company: str,
        broker: str,
        report_date: date,
        file_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> AnalystReportUploadResponse: ...

    @abstractmethod
    def list_for_company(self, symbol: str) -> list[AnalystReport]: ...

    @abstractmethod
    def get_sentiment(self, symbol: str) -> CompanySentiment: ...


class SyncAnalystReportService(AnalystReportService):
    """Forwards analyst reports to ledger-lens-sync and reads them back over REST."""

    def __init__(self, sync_client: SyncServiceClient) -> None:
        self._sync_client = sync_client

    def upload(
        self,
        company: str,
        broker: str,
        report_date: date,
        file_bytes: bytes,
        filename: str,
        content_type: str,
    ) -> AnalystReportUploadResponse:
        report = self._sync_client.create_analyst_report(
            company_symbol=company.upper(),
            file_bytes=file_bytes,
            filename=filename or "report.pdf",
            content_type=content_type or "application/octet-stream",
            broker_name=broker,
            report_date=report_date.isoformat(),
        )
        # Sync returns the persisted report; RAG/sentiment scoring runs asynchronously.
        return AnalystReportUploadResponse(report_id=str(report["id"]), status="processing")

    def list_for_company(self, symbol: str) -> list[AnalystReport]:
        response = self._sync_client.list_analyst_reports(symbol.upper())
        return [_to_report(r) for r in response.get("analyst_reports", [])]

    def get_sentiment(self, symbol: str) -> CompanySentiment:
        response = self._sync_client.list_analyst_reports(symbol.upper())
        reports = response.get("analyst_reports", [])
        scores = [r["sentiment_score"] for r in reports if r.get("sentiment_score") is not None]
        # sentiment_score is normalized 0..1; bucket into sell / hold / buy thirds.
        buy = sum(1 for s in scores if s > 0.66)
        sell = sum(1 for s in scores if s < 0.33)
        hold = len(scores) - buy - sell
        score = sum(scores) / len(scores) if scores else 0.5
        return CompanySentiment(
            symbol=symbol.upper(),
            buy=buy,
            hold=hold,
            sell=sell,
            score=score,
            reports_count=len(reports),
        )


def _to_report(report: JsonObject) -> AnalystReport:
    return AnalystReport(
        report_id=str(report["id"]),
        broker=report.get("broker_name") or "",
        date=report["report_date"],
        sentiment_score=report.get("sentiment_score"),
    )