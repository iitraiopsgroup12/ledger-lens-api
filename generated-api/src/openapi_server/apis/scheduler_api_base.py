# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.error_response import ErrorResponse
from openapi_server.models.scheduler_run_response import SchedulerRunResponse
from openapi_server.models.scheduler_status import SchedulerStatus
from openapi_server.security_api import get_token_bearerAuth

class BaseSchedulerApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseSchedulerApi.subclasses = BaseSchedulerApi.subclasses + (cls,)
    async def run_scheduler(
        self,
    ) -> SchedulerRunResponse:
        """Trigger scheduler execution manually."""
        ...


    async def get_scheduler_status(
        self,
    ) -> SchedulerStatus:
        """Retrieve current scheduler execution status."""
        ...
