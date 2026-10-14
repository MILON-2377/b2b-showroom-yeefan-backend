from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class ProductColorDTO:
    id: UUID
    product_id: UUID
    name: str
    sort_order: int
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CreateProductColorDTO:
    name: str
    sort_order: int = 0



@dataclass(frozen=True)
class UpdateProductColorDTO:
    id: UUID | None
    name: str
    sort_order: int