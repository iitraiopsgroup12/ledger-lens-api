"""Auth module business logic.

This proxy holds no user store of its own: credentials and roles live in
ledger-lens-sync's `/users` resource (see docs/servers/ledger-lens-sync.json).
`AuthService` only resolves *who* a caller is.
"""

from abc import ABC, abstractmethod

from app.clients.sync_client import SyncServiceClient
from app.schemas.auth import LoginResponse, UserProfile
from app.services.exceptions import NotFoundError


class AuthService(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> LoginResponse: ...

    @abstractmethod
    def get_profile(self, user_id: str) -> UserProfile: ...


class SyncAuthService(AuthService):
    """Resolves users against ledger-lens-sync; issues no real JWT yet.

    TODO: ledger-lens-sync's `/users` resource has no password-verification
    endpoint, so login cannot validate a password remotely yet. Once sync
    exposes a credentials-check endpoint, wire it in here instead of the
    email-lookup placeholder below.
    """

    def __init__(self, sync_client: SyncServiceClient) -> None:
        self._sync_client = sync_client

    def login(self, email: str, password: str) -> LoginResponse:
        users = self._sync_client.list_users(limit=500)
        user = next((u for u in users if u["email"] == email), None)
        if user is None:
            raise NotFoundError(f"No user found for email '{email}'")
        # TODO: sign a real JWT containing user_id, role, exp (24h); for now the
        # caller's user_id doubles as the bearer token (see deps.get_current_user).
        return LoginResponse(
            access_token=str(user["id"]),
            user={"id": str(user["id"]), "name": user.get("full_name") or user["email"]},
        )

    def get_profile(self, user_id: str) -> UserProfile:
        try:
            user = self._sync_client.get_user(int(user_id))
        except (ValueError, NotFoundError) as exc:
            raise NotFoundError(f"No user found for id '{user_id}'") from exc
        return UserProfile(id=str(user["id"]), email=user["email"], role=user["role"])
