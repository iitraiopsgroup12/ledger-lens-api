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


def get_settings() -> Settings:
    return Settings(
        sync_service_url=os.environ.get("LEDGER_LENS_SYNC_URL", "http://ledger-lens-sync"),
        rag_service_url=os.environ.get("LEDGER_LENS_RAG_URL", "http://ledger-lens-rag"),
        request_timeout_seconds=float(os.environ.get("BACKEND_REQUEST_TIMEOUT_SECONDS", "10")),
    )