from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.inquiries.models.inquiry import Inquiry


class AbstractInquiryRepository(ABC):
    @abstractmethod
    async def update_status(
        self,
        inquiry: Inquiry
    ) -> Inquiry:
        raise NotImplementedError

    @abstractmethod
    async def create(self, inquiry: Inquiry) -> Inquiry:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        inquiry_id: UUID,
    ) -> Inquiry | None:
        raise NotImplementedError

    @abstractmethod
    async def list_admin(
        self,
        *,
        offset: int,
        limit: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> list[Inquiry]:
        raise NotImplementedError

    @abstractmethod
    async def count_admin(
        self,
        *,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> int:
        raise NotImplementedError
