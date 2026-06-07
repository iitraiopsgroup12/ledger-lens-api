# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.error_response import ErrorResponse  # noqa: F401
from openapi_server.models.mcp_announcement import MCPAnnouncement  # noqa: F401
from openapi_server.models.refresh_response import RefreshResponse  # noqa: F401


def test_get_announcements(client: TestClient):
    """Test case for get_announcements

    Get corporate announcements
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/mcp/{symbol}/announcements".format(symbol='TCS'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_refresh_company(client: TestClient):
    """Test case for refresh_company

    Refresh company data
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/mcp/{symbol}/refresh".format(symbol='TCS'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

