"""Version 1 API routers, aggregated into a single ``api_router``."""

from fastapi import APIRouter

from app.api.v1 import (
    analyst_reports,
    auth,
    chat,
    companies,
    dashboard,
    documents,
    kpi,
    onboard,
    scheduler,
    watchlist,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(companies.router)
api_router.include_router(watchlist.router)
api_router.include_router(documents.router)
api_router.include_router(onboard.router)
api_router.include_router(chat.router)
api_router.include_router(kpi.router)
api_router.include_router(analyst_reports.router)
api_router.include_router(dashboard.router)
api_router.include_router(scheduler.router)
