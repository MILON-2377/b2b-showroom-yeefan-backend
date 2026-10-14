from uuid import UUID

from app.core.errors.base import ConflictError, NotFoundError, ValidationError


class ProductCodeAlreadyExistsError(ConflictError):
    """Raised when a product code already exists for a brand."""

    def __init__(self, product_code: str) -> None:
        super().__init__(
            "Product code already exists",
            code="PRODUCT_CODE_ALREADY_EXISTS",
        )
        self.product_code = product_code


class ProductSlugAlreadyExistsError(ConflictError):
    """Raised when a product slug already exists for a brand."""

    def __init__(self, slug: str) -> None:
        super().__init__(
            "Product slug already exists",
            code="PRODUCT_SLUG_ALREADY_EXISTS",
        )
        self.slug = slug


class ProductNotFoundError(NotFoundError):
    """Raised when a product does not exist."""

    def __init__(self, product_id: UUID) -> None:
        super().__init__(
            "Product not found",
            code="PRODUCT_NOT_FOUND",
        )
        self.product_id = product_id


class InvalidProductCursorError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            message="The product cursor is invalid.",
            code="INVALID_PRODUCT_CURSOR",
        )
