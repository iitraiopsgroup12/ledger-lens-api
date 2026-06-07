# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import List
from typing_extensions import Annotated
from openapi_server.models.error_response import ErrorResponse
from openapi_server.models.inline_object import InlineObject
from openapi_server.models.watchlist import Watchlist
from openapi_server.models.watchlist_delete_response import WatchlistDeleteResponse
from openapi_server.models.watchlist_item import WatchlistItem
from openapi_server.models.watchlist_request import WatchlistRequest
from openapi_server.models.watchlist_update_request import WatchlistUpdateRequest
from openapi_server.security_api import get_token_bearerAuth

class BaseWatchlistApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseWatchlistApi.subclasses = BaseWatchlistApi.subclasses + (cls,)
    async def get_watchlist(
        self,
    ) -> List[WatchlistItem]:
        """Get all watchlist entries for the authenticated user."""
        ...


    async def create_watchlist(
        self,
        watchlist_request: WatchlistRequest,
    ) -> Watchlist:
        """Add a company to the authenticated user&#39;s watchlist with a refresh frequency."""
        ...


    async def update_watchlist(
        self,
        symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")],
        watchlist_update_request: WatchlistUpdateRequest,
    ) -> InlineObject:
        """Update the refresh frequency for a watchlisted company."""
        ...


    async def delete_watchlist(
        self,
        symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")],
    ) -> WatchlistDeleteResponse:
        """Remove a company from the authenticated user&#39;s watchlist."""
        ...
