from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_company_service, get_current_user
from app.schemas.company import CompanyProfile, CompanySearchResult
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["Company"], dependencies=[Depends(get_current_user)])


@router.get("/search", response_model=CompanySearchResult)
def search_company(
    symbol: Annotated[str, Query()],
    company_service: Annotated[CompanyService, Depends(get_company_service)],
) -> CompanySearchResult:
    return company_service.search(symbol)


@router.get("/{symbol}", response_model=CompanyProfile)
def get_company(
    symbol: str,
    company_service: Annotated[CompanyService, Depends(get_company_service)],
) -> CompanyProfile:
    return company_service.get_profile(symbol)
