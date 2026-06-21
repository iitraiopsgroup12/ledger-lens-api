"""Comparison module business logic.

Per docs/API_Documentation.docx Flow 4: retrieves Pinecone chunks across
each requested company's namespace and asks Gemini to produce a
structured growth/risk/outlook breakdown grounded in those filings.
"""

from abc import ABC, abstractmethod

from app.schemas.compare import CompareResponse
from app.services.exceptions import NotFoundError


class CompareService(ABC):
    @abstractmethod
    def compare(self, companies: list[str]) -> CompareResponse: ...


class InMemoryCompareService(CompareService):
    """Placeholder implementation. TODO: wire to Pinecone multi-namespace retrieval + Gemini generation."""

    def __init__(self) -> None:
        self._known_companies = {"TCS", "INFOSYS", "INFY"}

    def compare(self, companies: list[str]) -> CompareResponse:
        missing = [c for c in companies if c.upper() not in self._known_companies]
        if missing:
            raise NotFoundError(f"No completed documents found for: {', '.join(missing)}")
        return CompareResponse(
            growth_strategy=f"{companies[0]} focuses on... while {companies[1]}...",
            risks=f"{companies[0]} faces... {companies[1]} highlights...",
            management_outlook="Both managements expressed...",
            sources=[{"company": c, "document": "Annual Report FY25"} for c in companies],
        )
