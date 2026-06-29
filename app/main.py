"""FastAPI app initialization, global middleware, and exception handlers."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.core.config import get_settings
from app.core.logging import RequestTracingMiddleware, configure_logging
from app.services.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    ProcessingError,
    ServiceError,
)

configure_logging()

app = FastAPI(
    title="LedgerLens.ai Platform API",
    description=(
        "Monitors NSE-listed companies, ingests annual reports and corporate "
        "announcements, processes them through a RAG pipeline, and enables "
        "AI-powered chat and comparison over company filings."
    ),
    version="1.0.0",
)

_STATUS_BY_ERROR: dict[type[ServiceError], int] = {
    AuthenticationError: 401,
    NotFoundError: 404,
    ConflictError: 409,
    ProcessingError: 422,
}

# Trace every HTTP request/response (added before CORS so it wraps the
# outermost layer and times the full request).
app.add_middleware(RequestTracingMiddleware)

# Allow all cross-origin requests (clients run in-cluster). `allow_origin_regex`
# matches any origin AND echoes it back, so credentialed requests work too —
# unlike `allow_origins=["*"]`, which the spec forbids pairing with credentials.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(ServiceError)
def handle_service_error(request: Request, exc: ServiceError) -> JSONResponse:
    status_code = next((code for error_type, code in _STATUS_BY_ERROR.items() if isinstance(exc, error_type)), 500)
    return JSONResponse(status_code=status_code, content={"error": exc.__class__.__name__, "message": str(exc)})


app.include_router(api_router, prefix="/api/v1")


@app.get("/healthz", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    # 30-minute keep-alive to match the 30-min backend request timeout
    # (BACKEND_REQUEST_TIMEOUT_SECONDS); long RAG/KPI calls hold the connection.
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        timeout_keep_alive=1800,
        log_level=get_settings().log_level.lower(),
    )
