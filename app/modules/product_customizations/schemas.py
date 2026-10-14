from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.product_customizations.dtos.product_customization import (
    ProductCustomizationDTO,
)
from app.modules.product_customizations.dtos.product_customization_option import (
    ProductCustomizationOptionDTO,
)
from app.modules.product_customizations.models.product_customization_option import (
    CustomizationOptionType,
)


class CreateProductCustomizationOptionRequest(BaseModel):
    option_type: CustomizationOptionType
    details: str | None = None
    sort_order: int = Field(default=0, ge=0)


class CreateProductCustomizationRequest(BaseModel):
    is_customizable: bool = False
    notes: str | None = None
    options: list[CreateProductCustomizationOptionRequest] = Field(default_factory=list)


class ProductCustomizationResponse(BaseModel):
    id: UUID
    product_id: UUID
    is_customizable: bool
    notes: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(
        cls,
        dto: ProductCustomizationDTO,
    ) -> Self:
        return cls(
            id=dto.id,
            product_id=dto.product_id,
            is_customizable=dto.is_customizable,
            notes=dto.notes,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )


class ProductCustomizationOptionResponse(BaseModel):
    id: UUID
    customization_id: UUID
    option_type: CustomizationOptionType
    details: str | None
    sort_order: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(
        cls,
        dto: ProductCustomizationOptionDTO,
    ) -> Self:
        return cls(
            id=dto.id,
            customization_id=dto.customization_id,
            option_type=dto.option_type,
            details=dto.details,
            sort_order=dto.sort_order,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )




class UpdateProductCustomizationRequest(BaseModel):
    is_customizable: bool
    notes: str | None = None