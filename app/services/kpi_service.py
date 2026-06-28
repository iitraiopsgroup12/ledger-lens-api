"""KPI human-in-the-loop chat business logic.

A thin authenticated pass-through to ledger-lens-rag's `/api/v1/kpi/chat`
and `/api/v1/kpi/approve` (see docs/servers/ledger-lens-rag.json): the caller
starts an analysis, which may pause `awaiting_approval`, then resumes it with
an approve/reject decision.
"""

from abc import ABC, abstractmethod
from typing import Any

from app.clients.rag_client import RagServiceClient
from app.schemas.kpi import KpiApproveRequest


class KpiService(ABC):
    @abstractmethod
    def chat(self, email: str, symbol: str, message: str, session_id: str | None) -> dict[str, Any]: ...

    @abstractmethod
    def approve(self, request: KpiApproveRequest) -> dict[str, Any]: ...


class RagKpiService(KpiService):
    """Forwards KPI chat/approve requests to ledger-lens-rag unchanged.

    The upstream payload is passed through verbatim — no intermediate
    Pydantic validation — since ledger-lens-rag's response shape (e.g. `kpis`
    can be a markdown string or a dict) is owned by that service, not us.
    """

    def __init__(self, rag_client: RagServiceClient) -> None:
        self._rag_client = rag_client

    def chat(self, email: str, symbol: str, message: str, session_id: str | None) -> dict[str, Any]:
        return self._rag_client.kpi_chat(
            email=email, symbol=symbol, message=message, session_id=session_id
        )

    def approve(self, request: KpiApproveRequest) -> dict[str, Any]:
        return self._rag_client.kpi_approve(request.model_dump(exclude_none=True))