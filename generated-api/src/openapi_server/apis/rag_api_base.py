# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field
from typing_extensions import Annotated
from uuid import UUID
from openapi_server.models.error_response import ErrorResponse
from openapi_server.models.rag_process_response import RAGProcessResponse
from openapi_server.models.rag_status_response import RAGStatusResponse
from openapi_server.security_api import get_token_bearerAuth

class BaseRAGApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseRAGApi.subclasses = BaseRAGApi.subclasses + (cls,)
    async def process_document(
        self,
        document_id: Annotated[UUID, Field(description="Document identifier")],
    ) -> RAGProcessResponse:
        """Trigger extraction, chunking, embedding generation, and vector indexing."""
        ...


    async def get_processing_status(
        self,
        document_id: Annotated[UUID, Field(description="Document identifier")],
    ) -> RAGStatusResponse:
        """Retrieve current processing status of a document."""
        ...
