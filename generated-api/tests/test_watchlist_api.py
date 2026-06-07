# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.error_response import ErrorResponse  # noqa: F401
from openapi_server.models.inline_object import InlineObject  # noqa: F401
from openapi_server.models.watchlist import Watchlist  # noqa: F401
from openapi_server.models.watchlist_delete_response import WatchlistDeleteResponse  # noqa: F401
from openapi_server.models.watchlist_item import WatchlistItem  # noqa: F401
from openapi_server.models.watchlist_request import WatchlistRequest  # noqa: F401
from openapi_server.models.watchlist_update_request import WatchlistUpdateRequest  # noqa: F401


def test_get_watchlist(client: TestClient):
    """Test case for get_watchlist

    Get watchlist
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/watchlist",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_create_watchlist(client: TestClient):
    """Test case for create_watchlist

    Add company to watchlist
    """
    watchlist_request = {"symbol":"symbol","frequency":"daily"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/watchlist",
    #    headers=headers,
    #    json=watchlist_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_watchlist(client: TestClient):
    """Test case for update_watchlist

    Update watchlist frequency
    """
    watchlist_update_request = {"frequency":"daily"}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/watchlist/{symbol}".format(symbol='TCS'),
    #    headers=headers,
    #    json=watchlist_update_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_watchlist(client: TestClient):
    """Test case for delete_watchlist

    Remove company from watchlist
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/watchlist/{symbol}".format(symbol='TCS'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

