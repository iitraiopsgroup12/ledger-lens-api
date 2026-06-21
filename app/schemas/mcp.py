from datetime import date

from pydantic import BaseModel


class Announcement(BaseModel):
    title: str
    pdf_url: str
    date: date


class RefreshResponse(BaseModel):
    status: str
    new_documents_found: int
    document_ids: list[str]
