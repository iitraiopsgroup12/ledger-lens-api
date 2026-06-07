# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.dashboard_response import DashboardResponse  # noqa: F401
from openapi_server.models.error_response import ErrorResponse  # noqa: F401


def test_get_dashboard(client: TestClient):
    """Test case for get_dashboard

    Get dashboard summary
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/dashboard",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

