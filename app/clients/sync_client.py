"""Typed client for the ledger-lens-sync backend (see docs/servers/ledger-lens-sync.json)."""

from typing import Any

from app.clients.base import BaseServiceClient

JsonObject = dict[str, Any]


class SyncServiceClient(BaseServiceClient):
    # -- users -----------------------------------------------------------
    def create_user(self, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("POST", "/users", json=payload, token=token).json()

    def list_users(self, *, skip: int = 0, limit: int = 100, token: str | None = None) -> list[JsonObject]:
        params = {"skip": skip, "limit": limit}
        return self.request("GET", "/users", params=params, token=token).json()

    def get_user(self, user_id: int, *, token: str | None = None) -> JsonObject:
        return self.request("GET", f"/users/{user_id}", token=token).json()

    def update_user(self, user_id: int, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("PATCH", f"/users/{user_id}", json=payload, token=token).json()

    def delete_user(self, user_id: int, *, token: str | None = None) -> None:
        self.request("DELETE", f"/users/{user_id}", token=token)

    # -- companies ---------------------------------------------------------
    def create_company(self, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("POST", "/companies", json=payload, token=token).json()

    def list_companies(self, *, skip: int = 0, limit: int = 100, token: str | None = None) -> list[JsonObject]:
        params = {"skip": skip, "limit": limit}
        return self.request("GET", "/companies", params=params, token=token).json()

    def get_company(self, company_id: int, *, token: str | None = None) -> JsonObject:
        return self.request("GET", f"/companies/{company_id}", token=token).json()

    def update_company(self, company_id: int, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("PATCH", f"/companies/{company_id}", json=payload, token=token).json()

    def delete_company(self, company_id: int, *, token: str | None = None) -> None:
        self.request("DELETE", f"/companies/{company_id}", token=token)

    # -- watchlists ----------------------------------------------------
    def create_watchlist(self, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("POST", "/watchlists", json=payload, token=token).json()

    def list_watchlists(self, *, skip: int = 0, limit: int = 100, token: str | None = None) -> list[JsonObject]:
        params = {"skip": skip, "limit": limit}
        return self.request("GET", "/watchlists", params=params, token=token).json()

    def get_watchlist(self, watchlist_id: int, *, token: str | None = None) -> JsonObject:
        return self.request("GET", f"/watchlists/{watchlist_id}", token=token).json()

    def update_watchlist(self, watchlist_id: int, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("PATCH", f"/watchlists/{watchlist_id}", json=payload, token=token).json()

    def delete_watchlist(self, watchlist_id: int, *, token: str | None = None) -> None:
        self.request("DELETE", f"/watchlists/{watchlist_id}", token=token)

    # -- documents -------------------------------------------------------
    def create_document(self, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("POST", "/documents", json=payload, token=token).json()

    def list_documents(self, *, skip: int = 0, limit: int = 100, token: str | None = None) -> list[JsonObject]:
        params = {"skip": skip, "limit": limit}
        return self.request("GET", "/documents", params=params, token=token).json()

    def get_document(self, document_id: int, *, token: str | None = None) -> JsonObject:
        return self.request("GET", f"/documents/{document_id}", token=token).json()

    def update_document(self, document_id: int, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("PATCH", f"/documents/{document_id}", json=payload, token=token).json()

    def delete_document(self, document_id: int, *, token: str | None = None) -> None:
        self.request("DELETE", f"/documents/{document_id}", token=token)

    # -- chunks ----------------------------------------------------------
    def create_chunk(self, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("POST", "/chunks", json=payload, token=token).json()

    def list_chunks(self, *, skip: int = 0, limit: int = 100, token: str | None = None) -> list[JsonObject]:
        params = {"skip": skip, "limit": limit}
        return self.request("GET", "/chunks", params=params, token=token).json()

    def get_chunk(self, chunk_id: int, *, token: str | None = None) -> JsonObject:
        return self.request("GET", f"/chunks/{chunk_id}", token=token).json()

    def update_chunk(self, chunk_id: int, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("PATCH", f"/chunks/{chunk_id}", json=payload, token=token).json()

    def delete_chunk(self, chunk_id: int, *, token: str | None = None) -> None:
        self.request("DELETE", f"/chunks/{chunk_id}", token=token)

    # -- analyst reports ------------------------------------------------
    def create_analyst_report(self, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("POST", "/analyst-reports", json=payload, token=token).json()

    def list_analyst_reports(self, *, skip: int = 0, limit: int = 100, token: str | None = None) -> list[JsonObject]:
        params = {"skip": skip, "limit": limit}
        return self.request("GET", "/analyst-reports", params=params, token=token).json()

    def get_analyst_report(self, report_id: int, *, token: str | None = None) -> JsonObject:
        return self.request("GET", f"/analyst-reports/{report_id}", token=token).json()

    def update_analyst_report(self, report_id: int, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("PATCH", f"/analyst-reports/{report_id}", json=payload, token=token).json()

    def delete_analyst_report(self, report_id: int, *, token: str | None = None) -> None:
        self.request("DELETE", f"/analyst-reports/{report_id}", token=token)

    # -- update logs -----------------------------------------------------
    def create_update_log(self, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("POST", "/update-logs", json=payload, token=token).json()

    def list_update_logs(self, *, skip: int = 0, limit: int = 100, token: str | None = None) -> list[JsonObject]:
        params = {"skip": skip, "limit": limit}
        return self.request("GET", "/update-logs", params=params, token=token).json()

    def get_update_log(self, log_id: int, *, token: str | None = None) -> JsonObject:
        return self.request("GET", f"/update-logs/{log_id}", token=token).json()

    def update_update_log(self, log_id: int, payload: JsonObject, *, token: str | None = None) -> JsonObject:
        return self.request("PATCH", f"/update-logs/{log_id}", json=payload, token=token).json()

    def delete_update_log(self, log_id: int, *, token: str | None = None) -> None:
        self.request("DELETE", f"/update-logs/{log_id}", token=token)

    # -- onboarding / health ----------------------------------------------
    def onboard_company(self, symbol: str, user_id: int, *, token: str | None = None) -> list[JsonObject]:
        params = {"symbol": symbol, "user_id": user_id}
        return self.request("GET", "/onboard", params=params, token=token).json()

    def health(self) -> JsonObject:
        return self.request("GET", "/health").json()
