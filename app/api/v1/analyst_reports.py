from datetime import date as date_type
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from app.api.deps import get_analyst_report_service, get_current_user
from app.schemas.analyst_report import AnalystReport, AnalystReportUploadResponse, CompanySentiment
from app.services.analyst_report_service import AnalystReportService

router = APIRouter(tags=["Analyst Report"], dependencies=[Depends(get_current_user)])


@router.post("/analyst-reports", response_model=AnalystReportUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_analyst_report(
    file: Annotated[UploadFile, File()],
    company: Annotated[str, Form()],
    broker: Annotated[str, Form()],
    report_date: Annotated[date_type, Form(alias="date")],
    analyst_report_service: Annotated[AnalystReportService, Depends(get_analyst_report_service)],
) -> AnalystReportUploadResponse:
    file_bytes = await file.read()
    return analyst_report_service.upload(company, broker, report_date, file_bytes)


@router.get("/companies/{symbol}/analyst-reports", response_model=list[AnalystReport])
def list_analyst_reports(
    symbol: str,
    analyst_report_service: Annotated[AnalystReportService, Depends(get_analyst_report_service)],
) -> list[AnalystReport]:
    return analyst_report_service.list_for_company(symbol)


@router.get("/companies/{symbol}/sentiment", response_model=CompanySentiment)
def get_company_sentiment(
    symbol: str,
    analyst_report_service: Annotated[AnalystReportService, Depends(get_analyst_report_service)],
) -> CompanySentiment:
    return analyst_report_service.get_sentiment(symbol)
