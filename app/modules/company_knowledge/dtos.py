from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.models import RecordStatus


class CreateCompanyKnowledgeDTO(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class UpdateCompanyKnowledgeDTO(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    category: str | None = Field(default=None, max_length=100)
    content: str | None = None
    status: RecordStatus | None = None


class CompanyKnowledgeDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    category: str
    content: str
    status: RecordStatus
    created_at: datetime
    updated_at: datetime
