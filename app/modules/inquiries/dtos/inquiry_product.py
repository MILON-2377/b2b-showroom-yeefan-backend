from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class CreateInquiryProductDTO:
    product_id: UUID
    quantity_requested: int | None = None
    notes: str | None = None


@dataclass(frozen=True)
class InquiryProductDTO:
    id: UUID
    inquiry_id: UUID
    product_id: UUID
    quantity_requested: int | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
