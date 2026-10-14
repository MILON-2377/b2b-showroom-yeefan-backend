from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.core.models import RecordStatus


@dataclass(frozen=True)
class BrandDTO:
    id: UUID
    name: str
    slug: str
    description: str | None
    status: RecordStatus
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class PublicBrandQueryDTO:
    page: int = 1
    page_size: int = 20
    search: str | None = None


@dataclass(frozen=True)
class PublicBrandListDTO:
    items: list[BrandDTO]
    total: int
    page: int
    page_size: int
    total_pages: int
