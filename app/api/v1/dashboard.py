from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_dashboard_service
from app.schemas.auth import UserProfile
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    dashboard_service: Annotated[DashboardService, Depends(get_dashboard_service)],
) -> DashboardResponse:
    return dashboard_service.get_summary(current_user.id)
