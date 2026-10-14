from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class ProductDetailDTO:
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



@dataclass(frozen=True)
class CreateProductDetailDTO:
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



@dataclass(frozen=True)
class UpdateProductDetailDTO:
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