from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.product_customizations.models.product_customization_option import (
    CustomizationOptionType,
)


@dataclass(frozen=True)
class ProductCustomizationOptionDTO:
    id: UUID
    customization_id: UUID
    option_type: CustomizationOptionType
    details: str | None
    sort_order: int
    created_at: datetime
    updated_at: datetime




@dataclass(frozen=True)
class CreateProductCustomizationOptionDTO:
    option_type: CustomizationOptionType
    details: str | None = None
    sort_order: int = 0