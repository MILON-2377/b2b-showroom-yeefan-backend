from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.core.models import RecordStatus


@dataclass(frozen=True)
class CreateCatalogDTO:
    collection_id: UUID
    pdf_media_asset_id: UUID
    cover_media_asset_id: UUID
    title: str
    description: str | None = None


@dataclass(frozen=True)
class UpdateCatalogDTO:
    pdf_media_asset_id: UUID | None = None
    cover_media_asset_id: UUID | None = None
    title: str | None = None
    status: RecordStatus | None = None
    description: str | None = None


@dataclass(frozen=True)
class CatalogDTO:
    id: UUID
    collection_id: UUID
    pdf_media_asset_id: UUID
    cover_media_asset_id: UUID
    title: str
    description: str | None
    status: RecordStatus
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class PublicCatalogDTO:
    id: UUID
    collection_id: UUID
    title: str
    description: str | None
    catalog_url: str
    cover_image_url: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class PublicCatalogQueryDTO:
    page: int = 1
    page_size: int = 12
    search: str | None = None
    collection_id: UUID | None = None
    sort_order: str = "desc"


@dataclass(frozen=True)
class PublicCatalogListDTO:
    items: list[PublicCatalogDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass(frozen=True)
class AdminCatalogQueryDTO:
    page: int = 1
    page_size: int = 12
    search: str | None = None
    collection_id: UUID | None = None
    status: RecordStatus | None = None
    sort_order: str = "desc"


@dataclass(frozen=True)
class AdminCatalogDTO:
    id: UUID
    collection_id: UUID
    pdf_media_asset_id: UUID
    cover_media_asset_id: UUID
    title: str
    description: str | None
    status: RecordStatus
    pdf_url: str
    cover_image_url: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class AdminCatalogListDTO:
    items: list[AdminCatalogDTO]
    total: int
    page: int
    page_size: int
    total_pages: int



@dataclass(frozen=True)
class CatalogDetailQueryDTO:
    id: UUID
    collection_id: UUID
    pdf_media_asset_id: UUID
    cover_media_asset_id: UUID
    title: str
    description: str | None
    status: RecordStatus
    pdf_url: str
    cover_image_url: str
    created_at: datetime
    updated_at: datetime