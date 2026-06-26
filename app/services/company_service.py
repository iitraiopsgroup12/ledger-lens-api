"""Company module business logic.

Per docs/API_Documentation.docx Flow 1: company search validates/enriches
metadata via the NSE MCP tool (nse_corporate_announcements) and persists
to the ``companies`` table when not already present.
"""

from abc import ABC, abstractmethod

from app.schemas.company import CompanyProfile, CompanySearchResult
from app.services.exceptions import NotFoundError


class CompanyService(ABC):
    @abstractmethod
    def search(self, symbol: str) -> CompanySearchResult: ...

    @abstractmethod
    def get_profile(self, symbol: str) -> CompanyProfile: ...


class InMemoryCompanyService(CompanyService):
    """Placeholder implementation. TODO: back with Postgres `companies` table + live MCP lookup fallback."""

    def __init__(self) -> None:
        self._companies: dict[str, dict] = {
            "TCS": {"company_name": "Tata Consultancy Services", "sector": "IT", "documents": 12},
            "INFY": {"company_name": "Infosys", "sector": "IT", "documents": 9},
        }

    def search(self, symbol: str) -> CompanySearchResult:
        symbol = symbol.upper()
        company = self._companies.get(symbol)
        if company is None:
            # TODO: fall back to a live MCP call (nse_corporate_announcements) to validate the symbol.
            raise NotFoundError(f"Company '{symbol}' not found")
        return CompanySearchResult(symbol=symbol, company_name=company["company_name"], sector=company["sector"])

    def get_profile(self, symbol: str) -> CompanyProfile:
        symbol = symbol.upper()
        company = self._companies.get(symbol)
        if company is None:
            raise NotFoundError(f"Company '{symbol}' not found")
        return CompanyProfile(
            symbol=symbol,
            name=company["company_name"],
            sector=company["sector"],
            documents=company["documents"],
            is_active=True,
        )
