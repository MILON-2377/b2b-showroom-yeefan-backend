from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .product_customization_option import CreateProductCustomizationOptionDTO


@dataclass(frozen=True)
class ProductCustomizationDTO:
    id: UUID
    product_id: UUID
    is_customizable: bool
    notes: str | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CreateProductCustomizationDTO:
    is_customizable: bool = False
    notes: str | None = None
    options: tuple[CreateProductCustomizationOptionDTO, ...] = ()



@dataclass(frozen=True)
class UpdateProductCustomizationDTO:
    is_customizable: bool
    notes: str | None