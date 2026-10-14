from uuid import UUID

from app.core.errors.base import NotFoundError


class InquiryNotFoundError(NotFoundError):
    def __init__(
        self,
        inquiry_id: UUID,
    ) -> None:
        super().__init__(
            "Inquiry not found",
            code="INQUIRY_NOT_FOUND",
        )
        self.inquiry_id = inquiry_id



class InquiryProductNotFoundError(NotFoundError):
    def __init__(
        self,
        inquiry_product_id: UUID,
    ) -> None:
        super().__init__(
            "Inquiry product not found",
            code="INQUIRY_PRODUCT_NOT_FOUND",
        )
        self.inquiry_product_id = inquiry_product_id