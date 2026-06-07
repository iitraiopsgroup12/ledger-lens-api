# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.chat_api_base import BaseChatApi
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
from typing import List
from openapi_server.models.chat_history_item import ChatHistoryItem
from openapi_server.models.chat_request import ChatRequest
from openapi_server.models.chat_response import ChatResponse
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/chat",
    responses={
        200: {"model": ChatResponse, "description": "Chat response generated successfully"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Chat"],
    summary="Submit chat query",
    response_model_by_alias=True,
)
async def chat(
    chat_request: ChatRequest = Body(None, description=""),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> ChatResponse:
    """Ask a financial question using the RAG system."""
    if not BaseChatApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseChatApi.subclasses[0]().chat(chat_request)


@router.get(
    "/chat/history",
    responses={
        200: {"model": List[ChatHistoryItem], "description": "Chat history retrieved successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Chat"],
    summary="Get chat history",
    response_model_by_alias=True,
)
async def get_chat_history(
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[ChatHistoryItem]:
    """Retrieve previous chat interactions for the authenticated user."""
    if not BaseChatApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseChatApi.subclasses[0]().get_chat_history()
