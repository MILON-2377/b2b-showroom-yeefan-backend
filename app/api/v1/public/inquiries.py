from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.core.contracts.services.inquiry import AbstractInquiryService
from app.core.security.rate_limiter import limiter
from app.modules.inquiries.dependencies import get_inquiry_service
from app.modules.inquiries.schemas import (
    CreateInquiryRequest,
    CreateInquiryResponse,
)
from app.modules.inquiries.services.inquiry import InquiryService

router = APIRouter(
    prefix="/inquiries",
)


@router.post(
    "",
    response_model=CreateInquiryResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")
async def create_inquiry(
    request: Request,
    payload: CreateInquiryRequest,
    inquiry_service: Annotated[AbstractInquiryService, Depends(get_inquiry_service)],
) -> CreateInquiryResponse:
    dto = await inquiry_service.create(
        payload=InquiryService._to_create_dto(payload),
    )

    return CreateInquiryResponse.from_dto(dto)
