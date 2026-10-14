from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.product_media.dtos import ProductMediaDTO, ProductMediaQueryDTO


class CreateProductMediaRequest(BaseModel):
    media_asset_id: UUID
    alt_text: str | None = None
    sort_order: int = Field(default=0, ge=0)
    is_primary: bool = False


class ProductMediaResponse(BaseModel):
    id: UUID
    product_id: UUID
    media_asset_id: UUID
    alt_text: str | None
    sort_order: int
    is_primary: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, dto: ProductMediaDTO) -> Self:
        return cls(
            id=dto.id,
            product_id=dto.product_id,
            media_asset_id=dto.media_asset_id,
            alt_text=dto.alt_text,
            sort_order=dto.sort_order,
            is_primary=dto.is_primary,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )


class ProductMediaQueryResponse(BaseModel):
    id: UUID
    media_asset_id: UUID
    alt_text: str | None
    url: str
    mime_type: str | None
    width: int | None
    height: int | None
    sort_order: int
    is_primary: bool

    @classmethod
    def from_dto(
        cls,
        dto: ProductMediaQueryDTO,
    ) -> Self:
        return cls(
            id=dto.id,
            media_asset_id=dto.media_asset_id,
            alt_text=dto.alt_text,
            url=dto.url,
            mime_type=dto.mime_type,
            width=dto.width,
            height=dto.height,
            sort_order=dto.sort_order,
            is_primary=dto.is_primary,
        )



class UpdateProductMediaRequest(BaseModel):
    id: UUID | None = None
    media_asset_id: UUID
    alt_text: str | None = None
    sort_order: int = Field(default=0, ge=0)
    is_primary: bool = False