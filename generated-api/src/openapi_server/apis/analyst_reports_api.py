# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.analyst_reports_api_base import BaseAnalystReportsApi
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
from datetime import date
from pydantic import Field, StrictBytes, StrictStr
from typing import List, Tuple, Union
from typing_extensions import Annotated
from openapi_server.models.analyst_report import AnalystReport
from openapi_server.models.analyst_report_upload_response import AnalystReportUploadResponse
from openapi_server.models.company_sentiment import CompanySentiment
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/analyst-reports",
    responses={
        201: {"model": AnalystReportUploadResponse, "description": "Analyst report uploaded successfully"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Analyst Reports"],
    summary="Upload analyst report",
    response_model_by_alias=True,
)
async def upload_analyst_report(
    file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]] = Form(None, description=""),
    company: StrictStr = Form(None, description=""),
    broker: StrictStr = Form(None, description=""),
    var_date: date = Form(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> AnalystReportUploadResponse:
    """Upload a broker analyst report PDF for processing."""
    if not BaseAnalystReportsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAnalystReportsApi.subclasses[0]().upload_analyst_report(file, company, broker, var_date)


@router.get(
    "/companies/{symbol}/analyst-reports",
    responses={
        200: {"model": List[AnalystReport], "description": "Analyst reports retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Analyst Reports"],
    summary="Get analyst reports",
    response_model_by_alias=True,
)
async def get_analyst_reports(
    symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")] = Path(..., description="NSE ticker symbol"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[AnalystReport]:
    """Retrieve analyst reports for a company."""
    if not BaseAnalystReportsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAnalystReportsApi.subclasses[0]().get_analyst_reports(symbol)


@router.get(
    "/companies/{symbol}/sentiment",
    responses={
        200: {"model": CompanySentiment, "description": "Company sentiment retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Analyst Reports"],
    summary="Get company sentiment",
    response_model_by_alias=True,
)
async def get_company_sentiment(
    symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")] = Path(..., description="NSE ticker symbol"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> CompanySentiment:
    """Retrieve aggregated analyst sentiment for a company."""
    if not BaseAnalystReportsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAnalystReportsApi.subclasses[0]().get_company_sentiment(symbol)
