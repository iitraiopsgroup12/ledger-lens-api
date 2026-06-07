# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.rag_api_base import BaseRAGApi
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
from pydantic import Field
from typing_extensions import Annotated
from uuid import UUID
from openapi_server.models.error_response import ErrorResponse
from openapi_server.models.rag_process_response import RAGProcessResponse
from openapi_server.models.rag_status_response import RAGStatusResponse
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/rag/process/{document_id}",
    responses={
        200: {"model": RAGProcessResponse, "description": "RAG processing started successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["RAG"],
    summary="Process document for RAG",
    response_model_by_alias=True,
)
async def process_document(
    document_id: Annotated[UUID, Field(description="Document identifier")] = Path(..., description="Document identifier"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> RAGProcessResponse:
    """Trigger extraction, chunking, embedding generation, and vector indexing."""
    if not BaseRAGApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRAGApi.subclasses[0]().process_document(document_id)


@router.get(
    "/rag/status/{document_id}",
    responses={
        200: {"model": RAGStatusResponse, "description": "RAG processing status retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["RAG"],
    summary="Get RAG processing status",
    response_model_by_alias=True,
)
async def get_processing_status(
    document_id: Annotated[UUID, Field(description="Document identifier")] = Path(..., description="Document identifier"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> RAGStatusResponse:
    """Retrieve current processing status of a document."""
    if not BaseRAGApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseRAGApi.subclasses[0]().get_processing_status(document_id)
