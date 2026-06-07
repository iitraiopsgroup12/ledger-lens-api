# coding: utf-8

from fastapi.testclient import TestClient


from typing import List  # noqa: F401
from openapi_server.models.chat_history_item import ChatHistoryItem  # noqa: F401
from openapi_server.models.chat_request import ChatRequest  # noqa: F401
from openapi_server.models.chat_response import ChatResponse  # noqa: F401
from openapi_server.models.error_response import ErrorResponse  # noqa: F401


def test_chat(client: TestClient):
    """Test case for chat

    Submit chat query
    """
    chat_request = {"query":"query"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/chat",
    #    headers=headers,
    #    json=chat_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_chat_history(client: TestClient):
    """Test case for get_chat_history

    Get chat history
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/chat/history",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

