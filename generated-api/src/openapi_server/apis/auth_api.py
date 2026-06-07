# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.auth_api_base import BaseAuthApi
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
from openapi_server.models.login_request import LoginRequest
from openapi_server.models.login_response import LoginResponse
from openapi_server.models.profile_response import ProfileResponse
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/auth/login",
    responses={
        200: {"model": LoginResponse, "description": "Login successful"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Auth"],
    summary="Authenticate user",
    response_model_by_alias=True,
)
async def auth_login(
    login_request: LoginRequest = Body(None, description=""),
) -> LoginResponse:
    """Authenticate a user and receive a JWT access token."""
    if not BaseAuthApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthApi.subclasses[0]().auth_login(login_request)


@router.get(
    "/auth/profile",
    responses={
        200: {"model": ProfileResponse, "description": "User profile retrieved successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Auth"],
    summary="Get authenticated user profile",
    response_model_by_alias=True,
)
async def get_profile(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> ProfileResponse:
    """Fetch the authenticated user&#39;s profile."""
    if not BaseAuthApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthApi.subclasses[0]().get_profile()
