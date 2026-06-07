# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.compare_request import CompareRequest
from openapi_server.models.compare_response import CompareResponse
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

class BaseCompareApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseCompareApi.subclasses = BaseCompareApi.subclasses + (cls,)
    async def compare_companies(
        self,
        compare_request: CompareRequest,
    ) -> CompareResponse:
        """Compare two or more companies using annual reports, filings, and extracted financial insights."""
        ...
