from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Query

from app.api.deps import get_current_user, get_onboard_service
from app.schemas.auth import UserProfile
from app.schemas.common import MessageResponse
from app.services.onboard_service import OnboardService

router = APIRouter(prefix="/onboard", tags=["Onboard"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=MessageResponse)
def onboard_company(
    symbol: Annotated[str, Query()],
    background_tasks: BackgroundTasks,
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    onboard_service: Annotated[OnboardService, Depends(get_onboard_service)],
) -> MessageResponse:
    background_tasks.add_task(onboard_service.start_onboarding, symbol, int(current_user.id), current_user.id)
    return MessageResponse(
        message="The Selected Company has been started onboard ! Please check in Watchlist after sometime!"
    )