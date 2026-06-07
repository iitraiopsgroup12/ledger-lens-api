# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from uuid import UUID  # noqa: F401
from openapi_server.models.document import Document  # noqa: F401
from openapi_server.models.document_details import DocumentDetails  # noqa: F401
from openapi_server.models.download_document_response import DownloadDocumentResponse  # noqa: F401
from openapi_server.models.error_response import ErrorResponse  # noqa: F401


def test_list_documents(client: TestClient):
    """Test case for list_documents

    List company documents
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/companies/{symbol}/documents".format(symbol='TCS'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_document(client: TestClient):
    """Test case for get_document

    Get document metadata
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/documents/{document_id}".format(document_id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_download_document(client: TestClient):
    """Test case for download_document

    Download document
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/documents/{document_id}/download".format(document_id=UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d')),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

