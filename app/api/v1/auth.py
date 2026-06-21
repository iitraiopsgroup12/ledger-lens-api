from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_auth_service, get_current_user
from app.schemas.auth import LoginRequest, LoginResponse, UserProfile
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginResponse:
    return auth_service.login(payload.email, payload.password)


@router.get("/profile", response_model=UserProfile)
def get_profile(current_user: Annotated[UserProfile, Depends(get_current_user)]) -> UserProfile:
    return current_user
