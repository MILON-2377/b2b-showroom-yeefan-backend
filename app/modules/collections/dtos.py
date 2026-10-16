from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.core.models import RecordStatus


@dataclass(frozen=True)
class CollectionDTO:
    id: UUID
    brand_id: UUID
    name: str
    slug: str
    description: str | None
    status: RecordStatus
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class PublicCollectionQueryDTO:
    page: int = 1
    page_size: int = 20
    search: str | None = None


@dataclass(frozen=True)
class PublicCollectionListDTO:
    items: list[CollectionDTO]
    total: int
    page: int
    page_size: int
    total_pages: int



@dataclass(frozen=True)
class AvailableCatalogCollectionsDTO:
    items: list[CollectionDTO]
    total: int
    page: int
    page_size: int