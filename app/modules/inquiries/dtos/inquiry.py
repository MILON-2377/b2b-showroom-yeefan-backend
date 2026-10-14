from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.inquiries.dtos.inquiry_product import (
    CreateInquiryProductDTO,
    InquiryProductDTO,
)
from app.modules.inquiries.models.inquiry import (
    InquiryStatus,
    InquiryType,
    QuantityRange,
)


@dataclass(frozen=True, slots=True)
class UpdateInquiryStatusDTO:
    status: InquiryStatus
    internal_notes: str | None 


@dataclass(frozen=True)
class CreateInquiryDTO:
    name: str
    email: str
    phone: str | None
    country: str | None
    company_name: str | None
    job_title: str | None
    inquiry_type: InquiryType
    quantity_range: QuantityRange | None
    message: str
    source_page: str | None
    products: tuple[CreateInquiryProductDTO, ...]


@dataclass(frozen=True)
class InquiryDTO:
    id: UUID
    name: str
    email: str
    phone: str | None
    country: str | None
    company_name: str | None
    job_title: str | None
    inquiry_type: InquiryType
    quantity_range: QuantityRange | None
    message: str
    source_page: str | None
    status: InquiryStatus
    internal_notes: str | None
    created_at: datetime
    updated_at: datetime
    products: tuple[InquiryProductDTO, ...]
