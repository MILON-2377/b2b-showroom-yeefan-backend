from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status

from app.core.contracts.services.inquiry import AbstractInquiryService
from app.core.security.rate_limiter import limiter
from app.modules.inquiries.dependencies import get_inquiry_service
from app.modules.inquiries.dtos.inquiry import InquiryDTO, UpdateInquiryStatusDTO
from app.modules.inquiries.models.inquiry import InquiryStatus
from app.modules.inquiries.schemas import (
    AdminInquiryListResponse,
    UpdateInquiryStatusRequest,
)

router = APIRouter(
    prefix="/inquiries",
    tags=["admin-inquiries"],
)


@router.patch(
    "/{inquiry_id}",
    response_model=InquiryDTO,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute")
async def update_inquiry_status(
    request: Request,
    inquiry_id: UUID,
    payload: UpdateInquiryStatusRequest,
    service: Annotated[
        AbstractInquiryService,
        Depends(get_inquiry_service),
    ],
) -> InquiryDTO:
    data = UpdateInquiryStatusDTO(
        status=payload.status,
        internal_notes=payload.internal_notes,
    )

    return await service.update_status(
        inquiry_id=inquiry_id,
        data=data,
    )


@router.get(
    "",
    response_model=AdminInquiryListResponse,
)
@limiter.limit("120/minute")
async def list_inquiries(
    request: Request,
    service: Annotated[
        AbstractInquiryService,
        Depends(get_inquiry_service),
    ],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    status: InquiryStatus | None = Query(None),
) -> AdminInquiryListResponse:
    items, total = await service.list_admin(
        page=page,
        page_size=page_size,
        search=search,
        status=status,
    )

    total_pages = (total + page_size - 1) // page_size

    return AdminInquiryListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get(
    "/{inquiry_id}",
    response_model=InquiryDTO,
)
@limiter.limit("120/minute")
async def get_inquiry(
    request: Request,
    inquiry_id: UUID,
    service: Annotated[
        AbstractInquiryService,
        Depends(get_inquiry_service),
    ],
) -> InquiryDTO:
    return await service.get_by_id(inquiry_id)
