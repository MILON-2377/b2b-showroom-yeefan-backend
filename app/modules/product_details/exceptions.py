from uuid import UUID

from app.core.errors.base import NotFoundError, ValidationError


class ProductDetailNotFoundError(NotFoundError):
    def __init__(self, product_id: UUID) -> None:
        super().__init__(
            message=f"Product details not found for product: {product_id}",
            code="PRODUCT_DETAIL_NOT_FOUND",
            details={
                "product_id": str(product_id),
            },
        )


class ProductDetailsCannotBeNullError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            "Product details cannot be null",
            code="PRODUCT_DETAILS_CANNOT_BE_NULL",
        )
