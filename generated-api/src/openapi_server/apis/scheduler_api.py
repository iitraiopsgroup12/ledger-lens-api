# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.scheduler_api_base import BaseSchedulerApi
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
from openapi_server.models.error_response import ErrorResponse
from openapi_server.models.scheduler_run_response import SchedulerRunResponse
from openapi_server.models.scheduler_status import SchedulerStatus
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/scheduler/run",
    responses={
        200: {"model": SchedulerRunResponse, "description": "Scheduler executed successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Scheduler"],
    summary="Run scheduler manually",
    response_model_by_alias=True,
)
async def run_scheduler(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> SchedulerRunResponse:
    """Trigger scheduler execution manually."""
    if not BaseSchedulerApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSchedulerApi.subclasses[0]().run_scheduler()


@router.get(
    "/scheduler/status",
    responses={
        200: {"model": SchedulerStatus, "description": "Scheduler status retrieved successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Scheduler"],
    summary="Get scheduler status",
    response_model_by_alias=True,
)
async def get_scheduler_status(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> SchedulerStatus:
    """Retrieve current scheduler execution status."""
    if not BaseSchedulerApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseSchedulerApi.subclasses[0]().get_scheduler_status()
