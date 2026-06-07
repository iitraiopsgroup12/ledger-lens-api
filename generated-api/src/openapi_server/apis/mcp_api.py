# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.mcp_api_base import BaseMCPApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictStr
from typing import List
from typing_extensions import Annotated
from openapi_server.models.error_response import ErrorResponse
from openapi_server.models.mcp_announcement import MCPAnnouncement
from openapi_server.models.refresh_response import RefreshResponse
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/mcp/{symbol}/announcements",
    responses={
        200: {"model": List[MCPAnnouncement], "description": "Corporate announcements retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["MCP"],
    summary="Get corporate announcements",
    response_model_by_alias=True,
)
async def get_announcements(
    symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")] = Path(..., description="NSE ticker symbol"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[MCPAnnouncement]:
    """Fetch latest NSE/BSE corporate announcements for a company."""
    if not BaseMCPApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMCPApi.subclasses[0]().get_announcements(symbol)


@router.post(
    "/mcp/{symbol}/refresh",
    responses={
        200: {"model": RefreshResponse, "description": "Company refresh completed successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["MCP"],
    summary="Refresh company data",
    response_model_by_alias=True,
)
async def refresh_company(
    symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")] = Path(..., description="NSE ticker symbol"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> RefreshResponse:
    """Trigger manual MCP refresh for announcements and documents."""
    if not BaseMCPApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseMCPApi.subclasses[0]().refresh_company(symbol)
