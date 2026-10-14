from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.product_colors.dtos import ProductColorDTO


class CreateProductColorRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    sort_order: int = Field(default=0, ge=0)


class ProductColorResponse(BaseModel):
    id: UUID
    product_id: UUID
    name: str
    sort_order: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, dto: ProductColorDTO) -> Self:
        return cls(
            id=dto.id,
            product_id=dto.product_id,
            name=dto.name,
            sort_order=dto.sort_order,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )






class UpdateProductColorRequest(BaseModel):
    id: UUID | None = None
    name: str = Field(min_length=1, max_length=100)
    sort_order: int = Field(default=0, ge=0)