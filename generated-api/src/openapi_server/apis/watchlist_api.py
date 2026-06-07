# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.watchlist_api_base import BaseWatchlistApi
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
from openapi_server.models.inline_object import InlineObject
from openapi_server.models.watchlist import Watchlist
from openapi_server.models.watchlist_delete_response import WatchlistDeleteResponse
from openapi_server.models.watchlist_item import WatchlistItem
from openapi_server.models.watchlist_request import WatchlistRequest
from openapi_server.models.watchlist_update_request import WatchlistUpdateRequest
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/watchlist",
    responses={
        200: {"model": List[WatchlistItem], "description": "Watchlist retrieved successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Watchlist"],
    summary="Get watchlist",
    response_model_by_alias=True,
)
async def get_watchlist(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[WatchlistItem]:
    """Get all watchlist entries for the authenticated user."""
    if not BaseWatchlistApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWatchlistApi.subclasses[0]().get_watchlist()


@router.post(
    "/watchlist",
    responses={
        201: {"model": Watchlist, "description": "Watchlist created successfully"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        409: {"model": ErrorResponse, "description": "Conflict"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Watchlist"],
    summary="Add company to watchlist",
    response_model_by_alias=True,
)
async def create_watchlist(
    watchlist_request: WatchlistRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Watchlist:
    """Add a company to the authenticated user&#39;s watchlist with a refresh frequency."""
    if not BaseWatchlistApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWatchlistApi.subclasses[0]().create_watchlist(watchlist_request)


@router.put(
    "/watchlist/{symbol}",
    responses={
        200: {"model": InlineObject, "description": "Watchlist updated successfully"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Watchlist"],
    summary="Update watchlist frequency",
    response_model_by_alias=True,
)
async def update_watchlist(
    symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")] = Path(..., description="NSE ticker symbol"),
    watchlist_update_request: WatchlistUpdateRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> InlineObject:
    """Update the refresh frequency for a watchlisted company."""
    if not BaseWatchlistApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWatchlistApi.subclasses[0]().update_watchlist(symbol, watchlist_update_request)


@router.delete(
    "/watchlist/{symbol}",
    responses={
        200: {"model": WatchlistDeleteResponse, "description": "Watchlist removed successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Watchlist"],
    summary="Remove company from watchlist",
    response_model_by_alias=True,
)
async def delete_watchlist(
    symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")] = Path(..., description="NSE ticker symbol"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> WatchlistDeleteResponse:
    """Remove a company from the authenticated user&#39;s watchlist."""
    if not BaseWatchlistApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseWatchlistApi.subclasses[0]().delete_watchlist(symbol)
