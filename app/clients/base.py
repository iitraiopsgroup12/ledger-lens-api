"""Shared HTTP plumbing for backend service clients.

The ledger-lens-sync / ledger-lens-rag services expose no auth scheme in
their specs, so requests are made without an Authorization header.
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
        **kwargs,
    ) -> httpx.Response:
        try:
            response = self._client.request(method, path, **kwargs)
        except httpx.RequestError as exc:
            raise ProcessingError(f"Upstream request to {self._client.base_url}{path} failed: {exc}") from exc
        if response.status_code >= 400:
            error_cls = _STATUS_TO_ERROR.get(response.status_code, ProcessingError)
            raise error_cls(f"{method} {path} -> {response.status_code}: {response.text}")
        return response

    def close(self) -> None:
        self._client.close()