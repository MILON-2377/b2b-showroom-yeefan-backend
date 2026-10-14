from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class ProductMediaDTO:
    id: UUID
    product_id: UUID
    media_asset_id: UUID
    alt_text: str | None
    sort_order: int
    is_primary: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CreateProductMediaDTO:
    media_asset_id: UUID
    alt_text: str | None = None
    sort_order: int = 0
    is_primary: bool = False



@dataclass(frozen=True)
class ProductListImageDTO:
    id: UUID
    url: str
    mime_type: str | None
    width: int | None
    height: int | None


@dataclass(frozen=True)
class ProductMediaQueryDTO:
    id: UUID
    media_asset_id: UUID
    alt_text: str | None
    url: str
    mime_type: str | None
    width: int | None
    height: int | None
    sort_order: int
    is_primary: bool



@dataclass(frozen=True)
class UpdateProductMediaDTO:
    id: UUID | None
    media_asset_id: UUID
    alt_text: str | None
    sort_order: int
    is_primary: bool