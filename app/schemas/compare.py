from pydantic import BaseModel, Field


class CompareRequest(BaseModel):
    companies: list[str] = Field(min_length=2)


class CompareSource(BaseModel):
    company: str
    document: str


class CompareResponse(BaseModel):
    growth_strategy: str
    risks: str
    management_outlook: str
    sources: list[CompareSource]
