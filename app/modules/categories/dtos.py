from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.core.models import RecordStatus


@dataclass(frozen=True)
class CreateCategoryDTO:
    name: str
    description: str | None = None
    status: RecordStatus = RecordStatus.DRAFT
    image_media_id: UUID | None = None


@dataclass(frozen=True)
class UpdateCategoryDTO:
    name: str | None = None
    description: str | None = None
    status: RecordStatus | None = None
    image_media_id: UUID | None = None


@dataclass(frozen=True)
class CategoryDTO:
    id: UUID
    name: str
    slug: str
    description: str | None
    status: RecordStatus
    image_media_id: UUID | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CategoryImageDTO:
    id: UUID
    url: str
    mime_type: str | None
    width: int | None
    height: int | None


@dataclass(frozen=True)
class CategoryListItem:
    id: UUID
    name: str
    slug: str
    description: str | None
    status: RecordStatus
    image: CategoryImageDTO | None
    created_at: datetime
    updated_at: datetime



# Publics
@dataclass(frozen=True)
class PublicCategoryDTO:
    id: UUID
    name: str
    slug: str
    status: RecordStatus
    image_id: UUID | None
    image_url: str | None


@dataclass(frozen=True)
class PublicCategoryListDTO:
    items: tuple[PublicCategoryDTO, ...]
    total: int