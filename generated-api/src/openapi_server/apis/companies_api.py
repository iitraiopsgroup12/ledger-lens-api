# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.companies_api_base import BaseCompaniesApi
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
from typing_extensions import Annotated
from openapi_server.models.company import Company
from openapi_server.models.company_details import CompanyDetails
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/companies/search",
    responses={
        200: {"model": Company, "description": "Company found successfully"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Companies"],
    summary="Search company by symbol",
    response_model_by_alias=True,
)
async def search_company(
    symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")] = Query(None, description="NSE ticker symbol", alias="symbol"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> Company:
    """Search for a company by its NSE ticker symbol."""
    if not BaseCompaniesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseCompaniesApi.subclasses[0]().search_company(symbol)


@router.get(
    "/companies/{symbol}",
    responses={
        200: {"model": CompanyDetails, "description": "Company details retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Companies"],
    summary="Get company profile",
    response_model_by_alias=True,
)
async def get_company(
    symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")] = Path(..., description="NSE ticker symbol"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> CompanyDetails:
    """Get full company profile including document count."""
    if not BaseCompaniesApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseCompaniesApi.subclasses[0]().get_company(symbol)
