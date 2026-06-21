"""RAG Processing module business logic.

Per docs/API_Documentation.docx section 5.2: extract text with PyMuPDF
(OCR fallback via pytesseract for scanned PDFs), chunk into ~500 tokens
with 50-token overlap, embed with Gemini text-embedding-004, and upsert
into a Pinecone namespace keyed by lowercase company symbol.
"""

from abc import ABC, abstractmethod

from app.schemas.rag import RagProcessResponse, RagStatusResponse
from app.services.exceptions import NotFoundError


class RagService(ABC):
    @abstractmethod
    def trigger_processing(self, document_id: str) -> RagProcessResponse: ...

    @abstractmethod
    def get_status(self, document_id: str) -> RagStatusResponse: ...


class InMemoryRagService(RagService):
    """Placeholder implementation. TODO: wire to the real extract -> chunk -> embed -> Pinecone pipeline."""

    def __init__(self) -> None:
        self._statuses: dict[str, dict] = {
            "uuid-789": {"status": "completed", "chunk_count": 142, "pinecone_namespace": "tcs"}
        }

    def trigger_processing(self, document_id: str) -> RagProcessResponse:
        self._statuses.setdefault(document_id, {"status": "pending", "chunk_count": None, "pinecone_namespace": None})
        self._statuses[document_id]["status"] = "processing"
        return RagProcessResponse(document_id=document_id, status="processing", message="Pipeline started")

    def get_status(self, document_id: str) -> RagStatusResponse:
        status = self._statuses.get(document_id)
        if status is None:
            raise NotFoundError(f"Document '{document_id}' not found")
        return RagStatusResponse(
            document_id=document_id,
            status=status["status"],
            chunk_count=status["chunk_count"],
            pinecone_namespace=status["pinecone_namespace"],
        )
