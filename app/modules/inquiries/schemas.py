from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.modules.inquiries.dtos.inquiry import InquiryDTO
from app.modules.inquiries.dtos.inquiry_product import (
    InquiryProductDTO,
)
from app.modules.inquiries.models.inquiry import (
    InquiryStatus,
    InquiryType,
    QuantityRange,
)


class AdminInquiryListResponse(BaseModel):
    items: list[InquiryDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


class CreateInquiryProductRequest(BaseModel):
    product_id: UUID
    quantity_requested: int | None = Field(default=None, gt=0)
    notes: str | None = None


class CreateInquiryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=50)
    country: str | None = Field(default=None, max_length=100)
    company_name: str | None = Field(default=None, max_length=255)
    job_title: str | None = Field(default=None, max_length=255)
    inquiry_type: InquiryType = InquiryType.GENERAL
    quantity_range: QuantityRange | None = None
    message: str = Field(min_length=1)
    source_page: str | None = None
    products: list[CreateInquiryProductRequest] = Field(default_factory=list)


class CreateInquiryResponse(BaseModel):
    id: UUID
    status: InquiryStatus
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: InquiryDTO) -> "CreateInquiryResponse":
        return cls(
            id=dto.id,
            status=dto.status,
            created_at=dto.created_at,
        )


class InquiryProductResponse(BaseModel):
    id: UUID
    inquiry_id: UUID
    product_id: UUID
    quantity_requested: int | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(
        cls,
        dto: InquiryProductDTO,
    ) -> "InquiryProductResponse":
        return cls(
            id=dto.id,
            inquiry_id=dto.inquiry_id,
            product_id=dto.product_id,
            quantity_requested=dto.quantity_requested,
            notes=dto.notes,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )


class InquiryResponse(BaseModel):
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
    products: list[InquiryProductResponse]

    @classmethod
    def from_dto(cls, dto: InquiryDTO) -> "InquiryResponse":
        return cls(
            id=dto.id,
            name=dto.name,
            email=dto.email,
            phone=dto.phone,
            country=dto.country,
            company_name=dto.company_name,
            job_title=dto.job_title,
            inquiry_type=dto.inquiry_type,
            quantity_range=dto.quantity_range,
            message=dto.message,
            source_page=dto.source_page,
            status=dto.status,
            internal_notes=dto.internal_notes,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            products=[
                InquiryProductResponse.from_dto(product) for product in dto.products
            ],
        )


class UpdateInquiryStatusRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: InquiryStatus
    internal_notes: str | None = None
