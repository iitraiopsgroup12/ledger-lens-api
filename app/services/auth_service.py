"""Auth module business logic.

This proxy holds no user store of its own: credentials and roles live in
ledger-lens-sync's `/users` resource (see docs/servers/ledger-lens-sync.json).
`AuthService` verifies credentials against that store and mints the JWT that
identifies the caller on every subsequent request.
"""

from abc import ABC, abstractmethod

from app.clients.sync_client import SyncServiceClient
from app.core.security import create_access_token, verify_password
from app.schemas.auth import LoginResponse, UserProfile
from app.services.exceptions import AuthenticationError, NotFoundError


class AuthService(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> LoginResponse: ...

    @abstractmethod
    def get_profile(self, user_id: str) -> UserProfile: ...


class SyncAuthService(AuthService):
    """Authenticates users against ledger-lens-sync and issues a JWT.

    Login looks the user up by email via `GET /users/email/{email_address}`,
    which returns the stored bcrypt `password_hash`, verifies the supplied
    password against it, and signs a 24h JWT embedding the user's identity.
    """

    def __init__(self, sync_client: SyncServiceClient) -> None:
        self._sync_client = sync_client

    def login(self, email: str, password: str) -> LoginResponse:
        try:
            user = self._sync_client.get_user_by_email(email)
        except NotFoundError:
            # Don't disclose whether the email exists; report a generic 401.
            raise AuthenticationError("Invalid email or password") from None
        if not verify_password(password, user["password_hash"]):
            raise AuthenticationError("Invalid email or password")
        name = user.get("full_name") or user["email"]
        token = create_access_token(
            user_id=str(user["id"]),
            email=user["email"],
            role=user["role"],
            name=name,
        )
        return LoginResponse(
            access_token=token,
            user={"id": str(user["id"]), "name": name},
        )

    def get_profile(self, user_id: str) -> UserProfile:
        try:
            user = self._sync_client.get_user(int(user_id))
        except (ValueError, NotFoundError) as exc:
            raise NotFoundError(f"No user found for id '{user_id}'") from exc
        return UserProfile(id=str(user["id"]), email=user["email"], role=user["role"])
