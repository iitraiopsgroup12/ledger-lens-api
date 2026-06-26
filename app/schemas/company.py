from pydantic import BaseModel


class CompanySearchResult(BaseModel):
    symbol: str
    company_name: str
    sector: str | None = None


class CompanyProfile(BaseModel):
    symbol: str
    name: str
    sector: str | None = None
    documents: int = 0
    is_active: bool = True
