from uuid import UUID

from app.core.errors.base import NotFoundError


class ProductColorNotFoundError(NotFoundError):
    def __init__(self, color_id: UUID) -> None:
        super().__init__(
            message=f"Product color not found: {color_id}",
            code="PRODUCT_COLOR_NOT_FOUND",
            details={
                "color_id": str(color_id),
            },
        )
