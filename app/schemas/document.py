from datetime import date
from typing import Literal

from pydantic import BaseModel

DocumentType = Literal["annual_report", "announcement", "other"]
ProcessingStatus = Literal["pending", "processing", "completed", "failed"]


class DocumentSummary(BaseModel):
    document_id: str
    title: str
    type: DocumentType
    report_year: str | None = None
    processing_status: ProcessingStatus
    upload_date: date | None = None


class DocumentDetails(BaseModel):
    id: str
    company_symbol: str
    title: str
    type: DocumentType
    s3_key: str | None = None
    processing_status: ProcessingStatus


class DownloadResponse(BaseModel):
    url: str
    expires_in: int
