from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class ProductMeasurementGuideDTO:
    id: UUID
    product_id: UUID
    title: str | None
    description: str | None
    measurement_unit: str
    notes: str | None
    created_at: datetime
    updated_at: datetime



@dataclass(frozen=True)
class CreateProductMeasurementGuideDTO:
    title: str | None = None
    description: str | None = None
    measurement_unit: str = "cm"
    notes: str | None = None



@dataclass(frozen=True)
class UpdateProductMeasurementGuideDTO:
    title: str | None
    description: str | None
    measurement_unit: str
    notes: str | None