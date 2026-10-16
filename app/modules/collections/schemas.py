from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.models import RecordStatus


class CreateCollectionRequest(BaseModel):
    brand_id: UUID
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: RecordStatus | None = None


class UpdateCollectionRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: RecordStatus | None = None


class CollectionResponse(BaseModel):
    id: UUID
    brand_id: UUID
    name: str
    slug: str
    description: str | None
    status: RecordStatus
    created_at: datetime
    updated_at: datetime


class CollectionListResponse(BaseModel):
    items: list[CollectionResponse]
    total: int
    page: int
    page_size: int


class PublicCollectionQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )


class PublicCollectionResponse(BaseModel):
    id: UUID
    brand_id: UUID
    name: str
    slug: str
    description: str | None
    created_at: datetime
    updated_at: datetime


class PublicCollectionListResponse(BaseModel):
    items: list[PublicCollectionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int



class AvailableCatalogCollectionsResponse(BaseModel):
    items: list[CollectionResponse]
    total: int
    page: int
    page_size: int