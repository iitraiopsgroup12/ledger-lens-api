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

    def health(self) -> JsonObject:
        return self.request("GET", "/api/v1/health").json()