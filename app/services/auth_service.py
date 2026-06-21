"""Auth module business logic.

Per docs/API_Documentation.docx section 5.4: JWT tokens should embed
user_id, role, and exp (24h). Real implementations must verify
signature/expiry (e.g. via python-jose) and hash passwords (e.g. via
passlib/bcrypt) against the ``users`` table in Postgres.
"""

from abc import ABC, abstractmethod

from app.schemas.auth import LoginResponse, UserProfile
from app.services.exceptions import NotFoundError


class AuthService(ABC):
    @abstractmethod
    def login(self, email: str, password: str) -> LoginResponse: ...

    @abstractmethod
    def get_profile(self, user_id: str) -> UserProfile: ...


class InMemoryAuthService(AuthService):
    """Placeholder implementation. TODO: replace with Postgres-backed auth + real JWT issuance."""

    def __init__(self) -> None:
        self._users: dict[str, dict] = {
            "user@company.com": {
                "id": "uuid-123",
                "name": "John Doe",
                "role": "analyst",
                "password": "******",
            }
        }

    def login(self, email: str, password: str) -> LoginResponse:
        user = self._users.get(email)
        if user is None or user["password"] != password:
            raise NotFoundError(f"No user found for email '{email}'")
        # TODO: sign a real JWT containing user_id, role, exp (24h).
        return LoginResponse(
            access_token="eyJhbGciOiJIUzI1NiIs...",
            user={"id": user["id"], "name": user["name"]},
        )

    def get_profile(self, user_id: str) -> UserProfile:
        for email, user in self._users.items():
            if user["id"] == user_id:
                return UserProfile(id=user["id"], email=email, role=user["role"])
        raise NotFoundError(f"No user found for id '{user_id}'")
