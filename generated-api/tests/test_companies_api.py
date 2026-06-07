# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.company import Company  # noqa: F401
from openapi_server.models.company_details import CompanyDetails  # noqa: F401
from openapi_server.models.error_response import ErrorResponse  # noqa: F401


def test_search_company(client: TestClient):
    """Test case for search_company

    Search company by symbol
    """
    params = [("symbol", 'TCS')]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/companies/search",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_company(client: TestClient):
    """Test case for get_company

    Get company profile
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/companies/{symbol}".format(symbol='TCS'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

