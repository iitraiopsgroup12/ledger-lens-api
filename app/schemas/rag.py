from typing import Literal

from pydantic import BaseModel

RagStatus = Literal["pending", "processing", "completed", "failed"]


class RagProcessResponse(BaseModel):
    document_id: str
    status: str
    message: str | None = None


class RagStatusResponse(BaseModel):
    document_id: str
    status: RagStatus
    chunk_count: int | None = None
    pinecone_namespace: str | None = None
