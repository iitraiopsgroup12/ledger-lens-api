"""Application logging setup and HTTP request-tracing middleware.

`configure_logging` wires the root logger (and uvicorn's loggers) to a single
format at the configured level (LOG_LEVEL, default DEBUG). `RequestTracingMiddleware`
emits a line per HTTP request/response so individual requests can be traced.
"""

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp

from app.core.config import get_settings

_LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"


def configure_logging() -> None:
    """Configure root and uvicorn loggers at the LOG_LEVEL from settings."""
    level = getattr(logging, get_settings().log_level, logging.DEBUG)

    logging.basicConfig(level=level, format=_LOG_FORMAT)

    # Align uvicorn's own loggers with our level/format so access and error
    # logs are emitted consistently (uvicorn configures these itself otherwise).
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(name).setLevel(level)


logger = logging.getLogger("ledger_lens.request")


class RequestTracingMiddleware(BaseHTTPMiddleware):
    """Log every HTTP request/response with a correlation id and latency."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", uuid.uuid4().hex)
        client = request.client.host if request.client else "-"
        logger.debug(
            "--> %s %s id=%s client=%s", request.method, request.url.path, request_id, client
        )

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "!! %s %s id=%s failed after %.1fms",
                request.method,
                request.url.path,
                request_id,
                elapsed_ms,
            )
            raise

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.debug(
            "<-- %s %s id=%s status=%s %.1fms",
            request.method,
            request.url.path,
            request_id,
            response.status_code,
            elapsed_ms,
        )
        response.headers["X-Request-ID"] = request_id
        return response