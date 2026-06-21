"""MCP Service module business logic.

Wraps the NSE MCP tool (nse_corporate_announcements) so the frontend and
scheduler have a consistent REST interface. Per docs/API_Documentation.docx
section 5.1, new announcements must be deduplicated against the
`documents` table using document_title + company_id as a composite key.
"""

from abc import ABC, abstractmethod
from uuid import uuid4

from app.schemas.mcp import Announcement, RefreshResponse


class McpService(ABC):
    @abstractmethod
    def get_announcements(self, symbol: str) -> list[Announcement]: ...

    @abstractmethod
    def refresh(self, symbol: str) -> RefreshResponse: ...


class InMemoryMcpService(McpService):
    """Placeholder implementation. TODO: call the real nse_corporate_announcements MCP tool."""

    def get_announcements(self, symbol: str) -> list[Announcement]:
        return [
            Announcement(
                title="Annual Report FY25",
                pdf_url="https://example.com/reports/annual_report_fy25.pdf",
                date="2026-05-15",
            )
        ]

    def refresh(self, symbol: str) -> RefreshResponse:
        # TODO: call MCP, diff against `documents`, download+upload new PDFs to S3,
        # create pending `documents` rows, and trigger RAG processing for each.
        return RefreshResponse(status="processing", new_documents_found=1, document_ids=[str(uuid4())])
