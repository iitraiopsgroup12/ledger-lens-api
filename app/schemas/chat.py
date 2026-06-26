from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str


class SourceCitation(BaseModel):
    document: str
    company: str
    page: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceCitation]


class ChatHistoryItem(BaseModel):
    query: str
    answer: str
    timestamp: datetime
