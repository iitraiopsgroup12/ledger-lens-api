# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import List
from typing_extensions import Annotated
from openapi_server.models.error_response import ErrorResponse
from openapi_server.models.mcp_announcement import MCPAnnouncement
from openapi_server.models.refresh_response import RefreshResponse
from openapi_server.security_api import get_token_bearerAuth

class BaseMCPApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseMCPApi.subclasses = BaseMCPApi.subclasses + (cls,)
    async def get_announcements(
        self,
        symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")],
    ) -> List[MCPAnnouncement]:
        """Fetch latest NSE/BSE corporate announcements for a company."""
        ...


    async def refresh_company(
        self,
        symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")],
    ) -> RefreshResponse:
        """Trigger manual MCP refresh for announcements and documents."""
        ...
