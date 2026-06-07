# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.error_response import ErrorResponse  # noqa: F401
from openapi_server.models.login_request import LoginRequest  # noqa: F401
from openapi_server.models.login_response import LoginResponse  # noqa: F401
from openapi_server.models.profile_response import ProfileResponse  # noqa: F401


def test_auth_login(client: TestClient):
    """Test case for auth_login

    Authenticate user
    """
    login_request = {"password":"password","email":"email"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/auth/login",
    #    headers=headers,
    #    json=login_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_profile(client: TestClient):
    """Test case for get_profile

    Get authenticated user profile
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/auth/profile",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

