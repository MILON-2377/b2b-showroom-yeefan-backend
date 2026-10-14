from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.models import RecordStatus
from app.modules.brands.query import BrandListQuery


class CreateBrandRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None


class BrandResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str | None
    logo_media_url: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class BrandListRequest(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    search: str | None = Field(default=None, min_length=1)
    status: RecordStatus | None = None

    def to_query(self) -> BrandListQuery:
        return BrandListQuery(
            page=self.page,
            page_size=self.page_size,
            search=self.search,
            status=self.status,
        )


class BrandListResponse(BaseModel):
    items: list[BrandResponse]
    total: int
    page: int
    page_size: int


class UpdateBrandRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: RecordStatus | None = None


class PublicBrandQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )


class PublicBrandResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class PublicBrandListResponse(BaseModel):
    items: list[PublicBrandResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
