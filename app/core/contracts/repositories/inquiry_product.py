from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.inquiries.models.inquiry_product import InquiryProduct


class AbstractInquiryProductRepository(ABC):
    @abstractmethod
    async def create_many(
        self,
        inquiry_products: list[InquiryProduct],
    ) -> list[InquiryProduct]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_inquiry_id(
        self,
        inquiry_id: UUID,
    ) -> list[InquiryProduct]:
        raise NotImplementedError
