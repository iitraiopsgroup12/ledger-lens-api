"""Password verification and JWT issuance/verification.

Passwords are never stored here: ledger-lens-sync owns the user store and
returns a bcrypt `password_hash` via `GET /users/email/{email_address}`. This
module only checks a plaintext password against that hash and mints/reads the
JWTs that carry the resulting identity on every subsequent request.
"""

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.core.config import get_settings
from app.schemas.auth import UserProfile
from app.services.exceptions import AuthenticationError


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Return True if `plain_password` matches the bcrypt `password_hash`."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        # Malformed/unsupported hash from upstream: treat as a failed check.
        return False


def create_access_token(*, user_id: str, email: str, role: str, name: str) -> str:
    """Sign a JWT embedding the caller's identity (see API docs section 5.4)."""
    settings = get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "name": name,
        "iat": now,
        "exp": now + timedelta(hours=settings.jwt_expiry_hours),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> UserProfile:
    """Verify a bearer JWT and return the identity it carries.

    Raises AuthenticationError on a missing/expired/invalid signature or claims.
    """
    settings = get_settings()
    try:
        claims = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise AuthenticationError("Missing or expired JWT token") from exc
    try:
        return UserProfile(id=claims["sub"], email=claims["email"], role=claims["role"])
    except KeyError as exc:
        raise AuthenticationError("JWT is missing required claims") from exc