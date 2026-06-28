"""Dependency injection providers.

Each `get_*_service` provider returns a process-wide singleton bound to
the service *interface*, so routers depend on abstractions rather than
concrete implementations (swap the placeholder for a real backend here).
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.clients.rag_client import RagServiceClient
from app.clients.sync_client import SyncServiceClient
from app.core.config import get_settings
from app.core.security import decode_access_token
from app.schemas.auth import UserProfile
from app.services.exceptions import AuthenticationError
from app.services.analyst_report_service import AnalystReportService, SyncAnalystReportService
from app.services.auth_service import AuthService, SyncAuthService
from app.services.chat_service import ChatService, RagChatService
from app.services.company_service import CompanyService, InMemoryCompanyService
from app.services.dashboard_service import DashboardService, InMemoryDashboardService
from app.services.document_service import DocumentService, SyncDocumentService
from app.services.kpi_service import KpiService, RagKpiService
from app.services.onboard_service import OnboardService, SyncOnboardService
from app.services.scheduler_service import InMemorySchedulerService, SchedulerService
from app.services.watchlist_service import SyncWatchlistService, WatchlistService

_bearer_scheme = HTTPBearer(auto_error=False)


@lru_cache
def get_sync_client() -> SyncServiceClient:
    settings = get_settings()
    return SyncServiceClient(settings.sync_service_url, settings.request_timeout_seconds)


@lru_cache
def get_rag_client() -> RagServiceClient:
    settings = get_settings()
    return RagServiceClient(settings.rag_service_url, settings.request_timeout_seconds)


@lru_cache
def get_auth_service() -> AuthService:
    return SyncAuthService(get_sync_client())


@lru_cache
def get_company_service() -> CompanyService:
    return InMemoryCompanyService()


@lru_cache
def get_watchlist_service() -> WatchlistService:
    return SyncWatchlistService(get_sync_client())


@lru_cache
def get_document_service() -> DocumentService:
    return SyncDocumentService(get_sync_client())


@lru_cache
def get_chat_service() -> ChatService:
    return RagChatService(get_rag_client())


@lru_cache
def get_kpi_service() -> KpiService:
    return RagKpiService(get_rag_client())


@lru_cache
def get_analyst_report_service() -> AnalystReportService:
    return SyncAnalystReportService(get_sync_client())


@lru_cache
def get_dashboard_service() -> DashboardService:
    return InMemoryDashboardService()


@lru_cache
def get_scheduler_service() -> SchedulerService:
    return InMemorySchedulerService()


@lru_cache
def get_onboard_service() -> OnboardService:
    return SyncOnboardService(get_sync_client())


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer_scheme)],
) -> UserProfile:
    """Resolve the caller's profile by verifying the Bearer JWT.

    The token is the one minted by `POST /auth/login`; its signature and
    expiry are checked and the embedded user_id/email/role claims (see API
    docs section 5.4) become the request identity. No upstream call is made.
    """
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or expired JWT token")
    try:
        return decode_access_token(credentials.credentials)
    except AuthenticationError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


def require_admin(current_user: Annotated[UserProfile, Depends(get_current_user)]) -> UserProfile:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Valid token but insufficient role")
    return current_user
