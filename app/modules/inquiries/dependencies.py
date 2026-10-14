from fastapi import Depends

from app.core.contracts.services.inquiry import AbstractInquiryService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.inquiries.services.inquiry import InquiryService
from app.shared.dependencies import get_uow


def get_inquiry_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractInquiryService:
    return InquiryService(uow=uow)
