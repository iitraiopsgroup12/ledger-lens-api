"""Backend service locations.

This API is a thin auth/authorization proxy in front of two in-cluster
backends reachable by their Kubernetes Service DNS names. Override via the
.env file (see .env.example) for local development (e.g. port-forwarded URLs).
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    sync_service_url: str
    rag_service_url: str
    request_timeout_seconds: float
    jwt_secret: str
    jwt_algorithm: str
    jwt_expiry_hours: int
    log_level: str


def get_settings() -> Settings:
    return Settings(
        sync_service_url=os.environ.get("LEDGER_LENS_SYNC_URL", "http://ledger-lens-sync"),
        rag_service_url=os.environ.get("LEDGER_LENS_RAG_URL", "http://ledger-lens-rag"),
        request_timeout_seconds=float(os.environ.get("BACKEND_REQUEST_TIMEOUT_SECONDS", "1800")),
        # JWT_SECRET must be overridden in every non-local environment; the default
        # is only safe for local development (see .env.example).
        jwt_secret=os.environ.get("JWT_SECRET", "dev-only-insecure-change-me-0123456789abcdef"),
        jwt_algorithm=os.environ.get("JWT_ALGORITHM", "HS256"),
        jwt_expiry_hours=int(os.environ.get("JWT_EXPIRY_HOURS", "24")),
        log_level=os.environ.get("LOG_LEVEL", "DEBUG").upper(),
    )