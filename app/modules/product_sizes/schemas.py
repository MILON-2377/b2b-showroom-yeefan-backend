from datetime import datetime
from decimal import Decimal
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.product_sizes.dtos.product_measurement_guide import (
    ProductMeasurementGuideDTO,
)
from app.modules.product_sizes.dtos.product_size import ProductSizeDTO


class CreateSizeMeasurementRequest(BaseModel):
    bust: Decimal | None = Field(default=None, ge=0)
    waist: Decimal | None = Field(default=None, ge=0)
    hips: Decimal | None = Field(default=None, ge=0)
    hollow_to_hem: Decimal | None = Field(default=None, ge=0)
    unit: str = Field(default="cm", min_length=1, max_length=10)


class CreateProductMeasurementGuideRequest(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None
    measurement_unit: str = Field(default="cm", min_length=1, max_length=10)
    notes: str | None = None


class CreateProductSizeRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    sort_order: int = Field(default=0, ge=0)
    measurement: CreateSizeMeasurementRequest | None = None


class ProductSizeResponse(BaseModel):
    id: UUID
    product_id: UUID
    name: str
    sort_order: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, dto: ProductSizeDTO) -> Self:
        return cls(
            id=dto.id,
            product_id=dto.product_id,
            name=dto.name,
            sort_order=dto.sort_order,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )


class ProductMeasurementGuideResponse(BaseModel):
    id: UUID
    product_id: UUID
    title: str | None
    description: str | None
    measurement_unit: str
    notes: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(
        cls,
        dto: ProductMeasurementGuideDTO,
    ) -> Self:
        return cls(
            id=dto.id,
            product_id=dto.product_id,
            title=dto.title,
            description=dto.description,
            measurement_unit=dto.measurement_unit,
            notes=dto.notes,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )



class UpdateProductSizeRequest(BaseModel):
    id: UUID | None = None
    name: str = Field(min_length=1, max_length=100)
    sort_order: int = Field(default=0, ge=0)



class UpdateProductMeasurementGuideRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    measurement_unit: str = Field(
        min_length=1,
        max_length=20,
    )
    notes: str | None = None