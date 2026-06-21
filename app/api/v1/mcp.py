from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_user, get_mcp_service
from app.schemas.mcp import Announcement, RefreshResponse
from app.services.mcp_service import McpService

router = APIRouter(prefix="/mcp", tags=["MCP Service"], dependencies=[Depends(get_current_user)])


@router.get("/{symbol}/announcements", response_model=list[Announcement])
def get_announcements(
    symbol: str,
    mcp_service: Annotated[McpService, Depends(get_mcp_service)],
) -> list[Announcement]:
    return mcp_service.get_announcements(symbol)


@router.post("/{symbol}/refresh", response_model=RefreshResponse, status_code=status.HTTP_202_ACCEPTED)
def refresh_company(
    symbol: str,
    mcp_service: Annotated[McpService, Depends(get_mcp_service)],
) -> RefreshResponse:
    return mcp_service.refresh(symbol)
