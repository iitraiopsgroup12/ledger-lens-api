from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user, get_rag_service
from app.schemas.rag import RagProcessResponse, RagStatusResponse
from app.services.rag_service import RagService

router = APIRouter(prefix="/rag", tags=["RAG Processing"], dependencies=[Depends(get_current_user)])


@router.post("/process/{document_id}", response_model=RagProcessResponse, status_code=status.HTTP_202_ACCEPTED)
def trigger_rag_processing(
    document_id: str,
    rag_service: Annotated[RagService, Depends(get_rag_service)],
) -> RagProcessResponse:
    return rag_service.trigger_processing(document_id)


@router.get("/status/{document_id}", response_model=RagStatusResponse)
def get_rag_status(
    document_id: str,
    rag_service: Annotated[RagService, Depends(get_rag_service)],
) -> RagStatusResponse:
    return rag_service.get_status(document_id)
