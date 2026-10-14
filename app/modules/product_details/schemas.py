from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel

from app.modules.product_details.dtos import ProductDetailDTO


class CreateProductDetailRequest(BaseModel):
    garment_type: str | None = None
    silhouette: str | None = None
    length: str | None = None
    fabric: str | None = None
    secondary_fabric: str | None = None
    lining: str | None = None
    neckline: str | None = None
    back_style: str | None = None
    waistline: str | None = None
    sleeve_type: str | None = None
    sleeve_length: str | None = None
    train: str | None = None
    embellishment: str | None = None
    closure: str | None = None
    internal_support: str | None = None


class ProductDetailResponse(BaseModel):
    id: UUID
    product_id: UUID
    garment_type: str | None
    silhouette: str | None
    length: str | None
    fabric: str | None
    secondary_fabric: str | None
    lining: str | None
    neckline: str | None
    back_style: str | None
    waistline: str | None
    sleeve_type: str | None
    sleeve_length: str | None
    train: str | None
    embellishment: str | None
    closure: str | None
    internal_support: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, dto: ProductDetailDTO) -> Self:
        return cls(
            id=dto.id,
            product_id=dto.product_id,
            garment_type=dto.garment_type,
            silhouette=dto.silhouette,
            length=dto.length,
            fabric=dto.fabric,
            secondary_fabric=dto.secondary_fabric,
            lining=dto.lining,
            neckline=dto.neckline,
            back_style=dto.back_style,
            waistline=dto.waistline,
            sleeve_type=dto.sleeve_type,
            sleeve_length=dto.sleeve_length,
            train=dto.train,
            embellishment=dto.embellishment,
            closure=dto.closure,
            internal_support=dto.internal_support,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )




class UpdateProductDetailRequest(BaseModel):
    garment_type: str | None = None
    silhouette: str | None = None
    length: str | None = None
    fabric: str | None = None
    secondary_fabric: str | None = None
    lining: str | None = None
    neckline: str | None = None
    back_style: str | None = None
    waistline: str | None = None
    sleeve_type: str | None = None
    sleeve_length: str | None = None
    train: str | None = None
    embellishment: str | None = None
    closure: str | None = None
    internal_support: str | None = None