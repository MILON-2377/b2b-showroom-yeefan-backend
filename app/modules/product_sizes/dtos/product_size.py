from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .size_measurement import CreateSizeMeasurementDTO


@dataclass(frozen=True)
class ProductSizeDTO:
    id: UUID
    product_id: UUID
    name: str
    sort_order: int
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CreateProductSizeDTO:
    name: str
    sort_order: int = 0


@dataclass(frozen=True)
class CreateProductSizeWithMeasurementDTO:
    size: CreateProductSizeDTO
    measurement: CreateSizeMeasurementDTO | None = None



@dataclass(frozen=True)
class UpdateProductSizeDTO:
    id: UUID | None
    name: str
    sort_order: int