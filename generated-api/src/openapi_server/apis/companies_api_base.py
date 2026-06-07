# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing_extensions import Annotated
from openapi_server.models.company import Company
from openapi_server.models.company_details import CompanyDetails
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

class BaseCompaniesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseCompaniesApi.subclasses = BaseCompaniesApi.subclasses + (cls,)
    async def search_company(
        self,
        symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")],
    ) -> Company:
        """Search for a company by its NSE ticker symbol."""
        ...


    async def get_company(
        self,
        symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")],
    ) -> CompanyDetails:
        """Get full company profile including document count."""
        ...
