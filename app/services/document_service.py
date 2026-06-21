"""Document module business logic.

Per docs/API_Documentation.docx Flow 3: documents are downloaded from
the MCP-provided pdf_url, uploaded to S3 (s3_key persisted), and carry a
processing_status of pending/processing/completed/failed.
"""

from abc import ABC, abstractmethod

from app.schemas.document import DocumentDetails, DocumentSummary, DownloadResponse
from app.services.exceptions import NotFoundError


class DocumentService(ABC):
    @abstractmethod
    def list_for_company(self, symbol: str) -> list[DocumentSummary]: ...

    @abstractmethod
    def get(self, document_id: str) -> DocumentDetails: ...

    @abstractmethod
    def get_download_url(self, document_id: str) -> DownloadResponse: ...


class InMemoryDocumentService(DocumentService):
    """Placeholder implementation. TODO: back with the Postgres `documents` table + S3 pre-signed URLs."""

    def __init__(self) -> None:
        self._documents: dict[str, dict] = {
            "uuid-789": {
                "company_symbol": "TCS",
                "title": "Annual Report FY25",
                "type": "annual_report",
                "report_year": "FY25",
                "s3_key": "tcs/fy25/annual_report.pdf",
                "processing_status": "completed",
                "upload_date": "2026-05-10",
            }
        }

    def list_for_company(self, symbol: str) -> list[DocumentSummary]:
        symbol = symbol.upper()
        return [
            DocumentSummary(
                document_id=doc_id,
                title=doc["title"],
                type=doc["type"],
                report_year=doc["report_year"],
                processing_status=doc["processing_status"],
                upload_date=doc["upload_date"],
            )
            for doc_id, doc in self._documents.items()
            if doc["company_symbol"] == symbol
        ]

    def get(self, document_id: str) -> DocumentDetails:
        doc = self._documents.get(document_id)
        if doc is None:
            raise NotFoundError(f"Document '{document_id}' not found")
        return DocumentDetails(
            id=document_id,
            company_symbol=doc["company_symbol"],
            title=doc["title"],
            type=doc["type"],
            s3_key=doc["s3_key"],
            processing_status=doc["processing_status"],
        )

    def get_download_url(self, document_id: str) -> DownloadResponse:
        doc = self._documents.get(document_id)
        if doc is None:
            raise NotFoundError(f"Document '{document_id}' not found")
        # TODO: generate a real pre-signed S3 URL valid for 1 hour.
        return DownloadResponse(url=f"https://s3.amazonaws.com/bucket/{doc['s3_key']}", expires_in=3600)
