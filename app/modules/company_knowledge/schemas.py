from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.models import RecordStatus


class CreateCompanyKnowledgeRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class UpdateCompanyKnowledgeRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1)
    status: RecordStatus | None = None


class CompanyKnowledgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    category: str
    content: str
    status: RecordStatus


class CompanyKnowledgeListResponse(BaseModel):
    items: list[CompanyKnowledgeResponse]
    total: int
    page: int
    page_size: int
