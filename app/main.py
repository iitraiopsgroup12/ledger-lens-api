"""FastAPI app initialization, global middleware, and exception handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1 import api_router
from app.services.exceptions import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    ProcessingError,
    ServiceError,
)

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

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
