from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.inquiries.dtos.inquiry import (
    CreateInquiryDTO,
    InquiryDTO,
    UpdateInquiryStatusDTO,
)


class AbstractInquiryService(ABC):
    @abstractmethod
    async def update_status(
        self,
        inquiry_id: UUID,
        data: UpdateInquiryStatusDTO,
    ) -> InquiryDTO:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        *,
        payload: CreateInquiryDTO,
    ) -> InquiryDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        inquiry_id: UUID,
    ) -> InquiryDTO:
        raise NotImplementedError

    @abstractmethod
    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> tuple[list[InquiryDTO], int]:
        raise NotImplementedError
