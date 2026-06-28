from typing import Annotated, Any

from fastapi import APIRouter, Depends, Form

from app.api.deps import get_current_user, get_kpi_service
from app.schemas.kpi import KpiApproveRequest
from app.services.kpi_service import KpiService

router = APIRouter(prefix="/kpi", tags=["KPI"], dependencies=[Depends(get_current_user)])


@router.post("/chat")
def kpi_chat(
    kpi_service: Annotated[KpiService, Depends(get_kpi_service)],
    email: Annotated[str, Form(min_length=1, description="User email — chat-memory session key")],
    symbol: Annotated[str, Form(min_length=1, description="Company stock symbol to analyze")],
    message: Annotated[str, Form(min_length=1, description="Natural-language KPI request")],
    session_id: Annotated[str | None, Form(description="Optional parallel thread for this email")] = None,
) -> dict[str, Any]:
    return kpi_service.chat(email, symbol, message, session_id)


@router.post("/approve")
def kpi_approve(
    payload: KpiApproveRequest,
    kpi_service: Annotated[KpiService, Depends(get_kpi_service)],
) -> dict[str, Any]:
    return kpi_service.approve(payload)