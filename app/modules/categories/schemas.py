from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.models import RecordStatus
from app.modules.categories.dtos import (
    CategoryListItem,
    PublicCategoryDTO,
)


class CreateCategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    status: RecordStatus = RecordStatus.DRAFT
    image_media_id: UUID | None = None


class UpdateCategoryRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: RecordStatus | None = None
    image_media_id: UUID | None = None


class CategoryImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    url: str
    mime_type: str | None
    width: int | None
    height: int | None


class CategoryListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    slug: str
    description: str | None
    status: RecordStatus
    image: CategoryImageResponse | None
    created_at: datetime
    updated_at: datetime


class CategoryListResponse(BaseModel):
    items: list[CategoryListItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    description: str | None
    image: CategoryImageResponse | None
    status: RecordStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, dto: CategoryListItem) -> Self:
        return cls(
            id=dto.id,
            name=dto.name,
            slug=dto.slug,
            description=dto.description,
            status=dto.status,
            image=(
                CategoryImageResponse(
                    id=dto.image.id,
                    url=dto.image.url,
                    mime_type=dto.image.mime_type,
                    width=dto.image.width,
                    height=dto.image.height,
                )
                if dto.image is not None
                else None
            ),
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )


# Publics
class PublicCategoryImageResponse(BaseModel):
    id: UUID
    url: str


class PublicCategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    image: PublicCategoryImageResponse | None

    @classmethod
    def from_dto(
        cls,
        dto: PublicCategoryDTO,
    ) -> "PublicCategoryResponse":
        return cls(
            id=dto.id,
            name=dto.name,
            slug=dto.slug,
            image=(
                PublicCategoryImageResponse(
                    id=dto.image_id,
                    url=dto.image_url,
                )
                if dto.image_id is not None and dto.image_url is not None
                else None
            ),
        )



class PublicCategoryListResponse(BaseModel):
    items: list[PublicCategoryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int