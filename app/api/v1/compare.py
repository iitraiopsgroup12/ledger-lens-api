from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_compare_service, get_current_user
from app.schemas.compare import CompareRequest, CompareResponse
from app.services.compare_service import CompareService

router = APIRouter(prefix="/compare", tags=["Comparison"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=CompareResponse)
def compare_companies(
    payload: CompareRequest,
    compare_service: Annotated[CompareService, Depends(get_compare_service)],
) -> CompareResponse:
    return compare_service.compare(payload.companies)
