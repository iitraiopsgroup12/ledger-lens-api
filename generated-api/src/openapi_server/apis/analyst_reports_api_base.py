# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from datetime import date
from pydantic import Field, StrictBytes, StrictStr
from typing import List, Tuple, Union
from typing_extensions import Annotated
from openapi_server.models.analyst_report import AnalystReport
from openapi_server.models.analyst_report_upload_response import AnalystReportUploadResponse
from openapi_server.models.company_sentiment import CompanySentiment
from openapi_server.models.error_response import ErrorResponse
from openapi_server.security_api import get_token_bearerAuth

class BaseAnalystReportsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAnalystReportsApi.subclasses = BaseAnalystReportsApi.subclasses + (cls,)
    async def upload_analyst_report(
        self,
        file: Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]],
        company: StrictStr,
        broker: StrictStr,
        var_date: date,
    ) -> AnalystReportUploadResponse:
        """Upload a broker analyst report PDF for processing."""
        ...


    async def get_analyst_reports(
        self,
        symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")],
    ) -> List[AnalystReport]:
        """Retrieve analyst reports for a company."""
        ...


    async def get_company_sentiment(
        self,
        symbol: Annotated[StrictStr, Field(description="NSE ticker symbol")],
    ) -> CompanySentiment:
        """Retrieve aggregated analyst sentiment for a company."""
        ...
