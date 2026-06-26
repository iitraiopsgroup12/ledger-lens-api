from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, get_watchlist_service
from app.schemas.auth import UserProfile
from app.schemas.watchlist import WatchlistItem
from app.services.watchlist_service import WatchlistService

router = APIRouter(prefix="/watchlist", tags=["Watchlist"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[WatchlistItem])
def list_watchlist(
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    watchlist_service: Annotated[WatchlistService, Depends(get_watchlist_service)],
) -> list[WatchlistItem]:
    return watchlist_service.list_for_user(current_user.id)