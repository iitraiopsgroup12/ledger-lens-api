# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.error_response import ErrorResponse
from openapi_server.models.login_request import LoginRequest
from openapi_server.models.login_response import LoginResponse
from openapi_server.models.profile_response import ProfileResponse
from openapi_server.security_api import get_token_bearerAuth

class BaseAuthApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAuthApi.subclasses = BaseAuthApi.subclasses + (cls,)
    async def auth_login(
        self,
        login_request: LoginRequest,
    ) -> LoginResponse:
        """Authenticate a user and receive a JWT access token."""
        ...


    async def get_profile(
        self,
    ) -> ProfileResponse:
        """Fetch the authenticated user&#39;s profile."""
        ...
