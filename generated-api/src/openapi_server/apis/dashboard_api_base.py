# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.dashboard_response import DashboardResponse
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

class BaseDashboardApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDashboardApi.subclasses = BaseDashboardApi.subclasses + (cls,)
    async def get_dashboard(
        self,
    ) -> DashboardResponse:
        """Retrieve dashboard metrics, watchlist statistics, processing status, and recent updates."""
        ...
