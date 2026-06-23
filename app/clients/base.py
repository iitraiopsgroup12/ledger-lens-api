"""Shared HTTP plumbing for backend service clients.

Every call to ledger-lens-sync / ledger-lens-rag is made on behalf of an
authenticated caller, so the bearer token presented to this proxy is
forwarded as the `Authorization` header on the outgoing request.
"""

import httpx

from app.services.exceptions import ConflictError, NotFoundError, ProcessingError, ServiceError

_STATUS_TO_ERROR: dict[int, type[ServiceError]] = {
    404: NotFoundError,
    409: ConflictError,
    422: ProcessingError,
}


class BaseServiceClient:
    def __init__(self, base_url: str, timeout: float) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def request(
        self,
        method: str,
        path: str,
        *,
        token: str | None = None,
        **kwargs,
    ) -> httpx.Response:
        headers = kwargs.pop("headers", {}) or {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        try:
            response = self._client.request(method, path, headers=headers, **kwargs)
        except httpx.RequestError as exc:
            raise ProcessingError(f"Upstream request to {self._client.base_url}{path} failed: {exc}") from exc
        if response.status_code >= 400:
            error_cls = _STATUS_TO_ERROR.get(response.status_code, ProcessingError)
            raise error_cls(f"{method} {path} -> {response.status_code}: {response.text}")
        return response

    def close(self) -> None:
        self._client.close()