# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.dashboard_api_base import BaseDashboardApi
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
from openapi_server.models.dashboard_response import DashboardResponse
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/dashboard",
    responses={
        200: {"model": DashboardResponse, "description": "Dashboard data retrieved successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Dashboard"],
    summary="Get dashboard summary",
    response_model_by_alias=True,
)
async def get_dashboard(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> DashboardResponse:
    """Retrieve dashboard metrics, watchlist statistics, processing status, and recent updates."""
    if not BaseDashboardApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDashboardApi.subclasses[0]().get_dashboard()
