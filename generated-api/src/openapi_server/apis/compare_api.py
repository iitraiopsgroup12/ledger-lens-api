# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.compare_api_base import BaseCompareApi
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
from openapi_server.models.compare_request import CompareRequest
from openapi_server.models.compare_response import CompareResponse
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/compare",
    responses={
        200: {"model": CompareResponse, "description": "Company comparison generated successfully"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Compare"],
    summary="Compare companies",
    response_model_by_alias=True,
)
async def compare_companies(
    compare_request: CompareRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> CompareResponse:
    """Compare two or more companies using annual reports, filings, and extracted financial insights."""
    if not BaseCompareApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseCompareApi.subclasses[0]().compare_companies(compare_request)
