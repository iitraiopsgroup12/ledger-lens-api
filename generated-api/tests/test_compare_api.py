# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.compare_request import CompareRequest  # noqa: F401
from openapi_server.models.compare_response import CompareResponse  # noqa: F401
from openapi_server.models.error_response import ErrorResponse  # noqa: F401


def test_compare_companies(client: TestClient):
    """Test case for compare_companies

    Compare companies
    """
    compare_request = {"companies":["companies","companies"]}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/compare",
    #    headers=headers,
    #    json=compare_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

