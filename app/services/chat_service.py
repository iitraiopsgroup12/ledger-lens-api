"""Chat module business logic.

Per docs/API_Documentation.docx section 5.3: LangGraph performs intent
detection (single-company vs. multi-company), retrieves top-8 chunks per
company namespace from Pinecone, and Gemini generates a grounded answer
that must only use retrieved context and cite sources.

The ledger-lens-rag service (docs/servers/ledger-lens-rag.json) exposes
that retrieval + generation pipeline behind `POST /api/v1/query`, so
`ask()` forwards to it and maps the RAG response onto `ChatResponse`.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

from app.clients.rag_client import RagServiceClient
from app.schemas.chat import ChatHistoryItem, ChatResponse, SourceCitation

_NO_ANSWER = "No relevant information found in the ingested documents for this query."


class ChatService(ABC):
    @abstractmethod
    def ask(self, user_id: str, query: str) -> ChatResponse: ...

    @abstractmethod
    def get_history(self, user_id: str) -> list[ChatHistoryItem]: ...


class RagChatService(ChatService):
    """Forwards questions to the ledger-lens-rag query endpoint and keeps per-user history in memory."""

    def __init__(self, rag_client: RagServiceClient) -> None:
        self._rag_client = rag_client
        self._history: dict[str, list[ChatHistoryItem]] = {}

    def ask(self, user_id: str, query: str) -> ChatResponse:
        result = self._rag_client.query({"query": query, "generate_answer": True})
        response = ChatResponse(
            answer=result.get("answer") or _NO_ANSWER,
            sources=[_to_citation(source) for source in result.get("sources", [])],
        )
        self._history.setdefault(user_id, []).append(
            ChatHistoryItem(query=query, answer=response.answer, timestamp=datetime.now(timezone.utc))
        )
        return response

    def get_history(self, user_id: str) -> list[ChatHistoryItem]:
        return self._history.get(user_id, [])[-50:]


def _to_citation(source: dict[str, Any]) -> SourceCitation:
    metadata = source.get("metadata") or {}
    return SourceCitation(
        document=metadata.get("document") or metadata.get("source") or "",
        company=metadata.get("company") or metadata.get("symbol") or "",
        page=metadata.get("page"),
    )