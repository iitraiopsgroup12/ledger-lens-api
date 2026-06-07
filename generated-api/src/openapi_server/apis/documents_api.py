# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.documents_api_base import BaseDocumentsApi
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
from uuid import UUID
from openapi_server.models.document import Document
from openapi_server.models.document_details import DocumentDetails
from openapi_server.models.download_document_response import DownloadDocumentResponse
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/companies/{symbol}/documents",
    responses={
        200: {"model": List[Document], "description": "Documents retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Documents"],
    summary="List company documents",
    response_model_by_alias=True,
)
async def list_documents(
    symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")] = Path(..., description="NSE ticker symbol"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> List[Document]:
    """List all documents available for a company."""
    if not BaseDocumentsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDocumentsApi.subclasses[0]().list_documents(symbol)


@router.get(
    "/documents/{document_id}",
    responses={
        200: {"model": DocumentDetails, "description": "Document metadata retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Documents"],
    summary="Get document metadata",
    response_model_by_alias=True,
)
async def get_document(
    document_id: Annotated[UUID, Field(description="Document identifier")] = Path(..., description="Document identifier"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> DocumentDetails:
    """Retrieve document metadata and processing information."""
    if not BaseDocumentsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDocumentsApi.subclasses[0]().get_document(document_id)


@router.get(
    "/documents/{document_id}/download",
    responses={
        200: {"model": DownloadDocumentResponse, "description": "Download URL generated successfully"},
        404: {"model": ErrorResponse, "description": "Resource Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    tags=["Documents"],
    summary="Download document",
    response_model_by_alias=True,
)
async def download_document(
    document_id: Annotated[UUID, Field(description="Document identifier")] = Path(..., description="Document identifier"),
    token_bearerAuth: TokenModel = Security(
        get_token_bearerAuth
    ),
) -> DownloadDocumentResponse:
    """Generate a pre-signed URL to download the document."""
    if not BaseDocumentsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDocumentsApi.subclasses[0]().download_document(document_id)
