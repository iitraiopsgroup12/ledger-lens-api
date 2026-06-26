from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_document_service
from app.schemas.document import DocumentDetails, DocumentSummary, DownloadResponse
from app.services.document_service import DocumentService

router = APIRouter(tags=["Document"], dependencies=[Depends(get_current_user)])


@router.get("/companies/{symbol}/documents", response_model=list[DocumentSummary])
def list_company_documents(
    symbol: str,
    document_service: Annotated[DocumentService, Depends(get_document_service)],
) -> list[DocumentSummary]:
    return document_service.list_for_company(symbol)


@router.get("/documents/{document_id}", response_model=DocumentDetails)
def get_document(
    document_id: str,
    document_service: Annotated[DocumentService, Depends(get_document_service)],
) -> DocumentDetails:
    return document_service.get(document_id)


@router.get("/documents/{document_id}/download", response_model=DownloadResponse)
def download_document(
    document_id: str,
    document_service: Annotated[DocumentService, Depends(get_document_service)],
) -> DownloadResponse:
    return document_service.get_download_url(document_id)
