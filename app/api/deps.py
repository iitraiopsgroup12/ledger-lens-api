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
from app.schemas.auth import UserProfile
from app.services.analyst_report_service import AnalystReportService, InMemoryAnalystReportService
from app.services.auth_service import AuthService, SyncAuthService
from app.services.chat_service import ChatService, InMemoryChatService
from app.services.company_service import CompanyService, InMemoryCompanyService
from app.services.dashboard_service import DashboardService, InMemoryDashboardService
from app.services.document_service import DocumentService, InMemoryDocumentService
from app.services.onboard_service import OnboardService, SyncOnboardService
from app.services.scheduler_service import InMemorySchedulerService, SchedulerService
from app.services.watchlist_service import InMemoryWatchlistService, WatchlistService

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
    return InMemoryWatchlistService()


@lru_cache
def get_document_service() -> DocumentService:
    return InMemoryDocumentService()


@lru_cache
def get_chat_service() -> ChatService:
    return InMemoryChatService()


@lru_cache
def get_analyst_report_service() -> AnalystReportService:
    return InMemoryAnalystReportService()


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
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserProfile:
    """Resolve the caller's profile from a Bearer token.

    Placeholder: does not verify a real JWT signature/expiry yet. Per
    docs/API_Documentation.docx section 5.4, replace with proper JWT
    decoding (user_id, role, exp) once an issuer (e.g. python-jose) is
    wired into AuthService.
    """
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or expired JWT token")
    # TODO: decode/verify credentials.credentials as a JWT instead of treating it as a user_id.
    try:
        return auth_service.get_profile(credentials.credentials)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or expired JWT token") from exc


def require_admin(current_user: Annotated[UserProfile, Depends(get_current_user)]) -> UserProfile:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Valid token but insufficient role")
    return current_user
