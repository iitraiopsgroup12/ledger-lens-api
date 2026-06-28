"""Typed client for the ledger-lens-rag backend (see docs/servers/ledger-lens-rag.json)."""

from typing import Any

from app.clients.base import BaseServiceClient

JsonObject = dict[str, Any]


class RagServiceClient(BaseServiceClient):
    def ingest(self, payload: JsonObject) -> JsonObject:
        return self.request("POST", "/api/v1/ingest", json=payload).json()

    def ingest_file(
        self, files: list[tuple[str, bytes, str]], metadata: str | None = None
    ) -> JsonObject:
        upload = [("files", file) for file in files]
        data = {"metadata": metadata} if metadata is not None else None
        return self.request("POST", "/api/v1/ingest/file", data=data, files=upload).json()

    def query(self, payload: JsonObject) -> JsonObject:
        return self.request("POST", "/api/v1/query", json=payload).json()

    def query_with_file(self, data: JsonObject, file: tuple[str, bytes, str]) -> JsonObject:
        return self.request(
            "POST", "/api/v1/query-with-file", data=data, files={"file": file}
        ).json()

    # -- KPI human-in-the-loop chat -------------------------------------
    def kpi_chat(
        self, *, email: str, symbol: str, message: str, session_id: str | None = None
    ) -> JsonObject:
        """Initiate a KPI chat via `POST /api/v1/kpi/chat` (form-urlencoded)."""
        data = {"email": email, "symbol": symbol, "message": message}
        if session_id is not None:
            data["session_id"] = session_id
        return self.request("POST", "/api/v1/kpi/chat", data=data).json()

    def kpi_approve(self, payload: JsonObject) -> JsonObject:
        """Resume a paused KPI chat via `POST /api/v1/kpi/approve` (JSON)."""
        return self.request("POST", "/api/v1/kpi/approve", json=payload).json()

    def health(self) -> JsonObject:
        return self.request("GET", "/api/v1/health").json()