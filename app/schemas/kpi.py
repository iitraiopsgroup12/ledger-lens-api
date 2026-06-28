"""KPI human-in-the-loop chat schemas.

Mirrors the `/api/v1/kpi/chat` + `/api/v1/kpi/approve` contracts in
docs/servers/ledger-lens-rag.json. `chat` initiates an analysis that may pause
for human approval; `approve` resumes it with the reviewer's decision.
"""

from typing import Any

from pydantic import BaseModel, Field


class KpiApproveRequest(BaseModel):
    email: str = Field(min_length=1, description="User email — chat-memory session key")
    session_id: str = Field(min_length=1, description="Session/thread to resume")
    decision: str = Field(description="approve | reject")
    interrupt_id: str | None = Field(default=None, description="The pending interrupt id from the chat response")
    feedback: str | None = Field(default=None, description="Optional reviewer note, returned on reject")


class KpiChatResponse(BaseModel):
    session_id: str
    status: str = Field(description="completed | awaiting_approval | denied | error")
    company: dict[str, Any] | None = None
    kpis: dict[str, Any] | None = None
    message: str | None = None
    pending_approval: dict[str, Any] | None = Field(
        default=None, description="Present when status=awaiting_approval; carries interrupt_id + summary"
    )
    steps: list[dict[str, Any]] = Field(default_factory=list)
    took_ms: float = 0.0