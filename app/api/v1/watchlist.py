from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user, get_watchlist_service
from app.schemas.auth import UserProfile
from app.schemas.common import MessageResponse
from app.schemas.watchlist import (
    WatchlistCreateRequest,
    WatchlistEntry,
    WatchlistItem,
    WatchlistUpdateRequest,
    WatchlistUpdateResponse,
)
from app.services.watchlist_service import WatchlistService

router = APIRouter(prefix="/watchlist", tags=["Watchlist"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=WatchlistEntry, status_code=status.HTTP_201_CREATED)
def add_to_watchlist(
    payload: WatchlistCreateRequest,
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    watchlist_service: Annotated[WatchlistService, Depends(get_watchlist_service)],
) -> WatchlistEntry:
    return watchlist_service.add(current_user.id, payload.symbol, payload.frequency)


@router.get("", response_model=list[WatchlistItem])
def list_watchlist(
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    watchlist_service: Annotated[WatchlistService, Depends(get_watchlist_service)],
) -> list[WatchlistItem]:
    return watchlist_service.list_for_user(current_user.id)


@router.put("/{symbol}", response_model=WatchlistUpdateResponse)
def update_watchlist(
    symbol: str,
    payload: WatchlistUpdateRequest,
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    watchlist_service: Annotated[WatchlistService, Depends(get_watchlist_service)],
) -> WatchlistUpdateResponse:
    return watchlist_service.update_frequency(current_user.id, symbol, payload.frequency)


@router.delete("/{symbol}", response_model=MessageResponse)
def remove_from_watchlist(
    symbol: str,
    current_user: Annotated[UserProfile, Depends(get_current_user)],
    watchlist_service: Annotated[WatchlistService, Depends(get_watchlist_service)],
) -> MessageResponse:
    watchlist_service.remove(current_user.id, symbol)
    return MessageResponse(message=f"{symbol.upper()} removed from watchlist")
