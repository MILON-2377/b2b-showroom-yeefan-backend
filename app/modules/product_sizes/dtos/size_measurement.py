from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class SizeMeasurementDTO:
    id: UUID
    product_size_id: UUID
    bust: Decimal | None
    waist: Decimal | None
    hips: Decimal | None
    hollow_to_hem: Decimal | None
    unit: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CreateSizeMeasurementDTO:
    bust: Decimal | None = None
    waist: Decimal | None = None
    hips: Decimal | None = None
    hollow_to_hem: Decimal | None = None
    unit: str = "cm"
