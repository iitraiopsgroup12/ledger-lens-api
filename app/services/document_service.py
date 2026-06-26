"""Document module business logic.

Documents live in ledger-lens-sync's `/documents` resource (see
docs/servers/ledger-lens-sync.json). This service reads them over REST and
maps sync's `DocumentRead` (keyed by integer `company_id`) onto the API's
symbol-oriented schemas.
"""

from abc import ABC, abstractmethod
from datetime import date, datetime

from app.clients.sync_client import JsonObject, SyncServiceClient
from app.schemas.document import DocumentDetails, DocumentSummary, DownloadResponse
from app.services.exceptions import NotFoundError


class DocumentService(ABC):
    @abstractmethod
    def list_for_company(self, symbol: str) -> list[DocumentSummary]: ...

    @abstractmethod
    def get(self, document_id: str) -> DocumentDetails: ...

    @abstractmethod
    def get_download_url(self, document_id: str) -> DownloadResponse: ...


class SyncDocumentService(DocumentService):
    """Reads documents from ledger-lens-sync, resolving company symbols <-> ids.

    Sync exposes no company filter on `/documents` nor a symbol lookup on
    `/companies`, so listing for a company resolves the symbol against the
    company list and filters documents client-side.
    """

    def __init__(self, sync_client: SyncServiceClient) -> None:
        self._sync_client = sync_client

    def list_for_company(self, symbol: str) -> list[DocumentSummary]:
        symbol = symbol.upper()
        company = next(
            (c for c in self._sync_client.list_companies(limit=500) if c.get("symbol", "").upper() == symbol),
            None,
        )
        if company is None:
            raise NotFoundError(f"Company '{symbol}' not found")
        company_id = company["id"]
        return [
            _to_summary(doc)
            for doc in self._sync_client.list_documents(limit=500)
            if doc.get("company_id") == company_id
        ]

    def get(self, document_id: str) -> DocumentDetails:
        doc = self._fetch(document_id)
        try:
            company = self._sync_client.get_company(doc["company_id"])
        except NotFoundError:
            company = {}
        return _to_details(doc, company.get("symbol", ""))

    def get_download_url(self, document_id: str) -> DownloadResponse:
        doc = self._fetch(document_id)
        s3_key = doc.get("s3_key")
        if not s3_key:
            raise NotFoundError(f"Document '{document_id}' has no stored file")
        # TODO: generate a real pre-signed S3 URL valid for 1 hour.
        return DownloadResponse(url=f"https://s3.amazonaws.com/bucket/{s3_key}", expires_in=3600)

    def _fetch(self, document_id: str) -> JsonObject:
        try:
            return self._sync_client.get_document(int(document_id))
        except (ValueError, NotFoundError) as exc:
            raise NotFoundError(f"Document '{document_id}' not found") from exc


def _to_summary(doc: JsonObject) -> DocumentSummary:
    return DocumentSummary(
        document_id=str(doc["id"]),
        title=doc.get("document_title") or "",
        type=doc["document_type"],
        report_year=doc.get("report_year"),
        processing_status=doc["processing_status"],
        upload_date=_to_date(doc.get("upload_date")),
    )


def _to_date(value: str | None) -> date | None:
    """Coerce sync's datetime `upload_date` to a plain date (it carries a time)."""
    if not value:
        return None
    return datetime.fromisoformat(value).date()


def _to_details(doc: JsonObject, company_symbol: str) -> DocumentDetails:
    return DocumentDetails(
        id=str(doc["id"]),
        company_symbol=company_symbol,
        title=doc.get("document_title") or "",
        type=doc["document_type"],
        s3_key=doc.get("s3_key"),
        processing_status=doc["processing_status"],
    )