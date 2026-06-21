"""Chat module business logic.

Per docs/API_Documentation.docx section 5.3: LangGraph performs intent
detection (single-company vs. multi-company), retrieves top-8 chunks per
company namespace from Pinecone, and Gemini generates a grounded answer
that must only use retrieved context and cite sources.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timezone

from app.schemas.chat import ChatHistoryItem, ChatResponse


class ChatService(ABC):
    @abstractmethod
    def ask(self, user_id: str, query: str) -> ChatResponse: ...

    @abstractmethod
    def get_history(self, user_id: str) -> list[ChatHistoryItem]: ...


class InMemoryChatService(ChatService):
    """Placeholder implementation. TODO: wire to LangGraph intent routing + Pinecone retrieval + Gemini generation."""

    def __init__(self) -> None:
        self._history: dict[str, list[ChatHistoryItem]] = {}

    def ask(self, user_id: str, query: str) -> ChatResponse:
        # TODO: route intent, retrieve chunks, call Gemini, and only answer from retrieved context.
        response = ChatResponse(
            answer="No relevant information found in the ingested documents for this query.",
            sources=[],
        )
        self._history.setdefault(user_id, []).append(
            ChatHistoryItem(query=query, answer=response.answer, timestamp=datetime.now(timezone.utc))
        )
        return response

    def get_history(self, user_id: str) -> list[ChatHistoryItem]:
        return self._history.get(user_id, [])[-50:]
