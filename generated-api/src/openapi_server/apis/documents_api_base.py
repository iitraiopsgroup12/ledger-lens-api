# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import List
from typing_extensions import Annotated
from uuid import UUID
from openapi_server.models.document import Document
from openapi_server.models.document_details import DocumentDetails
from openapi_server.models.download_document_response import DownloadDocumentResponse
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

class BaseDocumentsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDocumentsApi.subclasses = BaseDocumentsApi.subclasses + (cls,)
    async def list_documents(
        self,
        symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")],
    ) -> List[Document]:
        """List all documents available for a company."""
        ...


    async def get_document(
        self,
        document_id: Annotated[UUID, Field(description="Document identifier")],
    ) -> DocumentDetails:
        """Retrieve document metadata and processing information."""
        ...


    async def download_document(
        self,
        document_id: Annotated[UUID, Field(description="Document identifier")],
    ) -> DownloadDocumentResponse:
        """Generate a pre-signed URL to download the document."""
        ...
