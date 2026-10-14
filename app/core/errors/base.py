from typing import Any
from uuid import UUID


class AppError(Exception):
    """Base class for expected application errors."""

    status_code = 500

    def __init__(
        self,
        message: str,
        *,
        code: str,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details


class ValidationError(AppError):
    """Raised when domain/application validation fails."""

    status_code = 400


class UnauthorizedError(AppError):
    """Raised when authentication is required or authentication failed."""

    status_code = 401


class ForbiddenError(AppError):
    """Raised when the authenticated user lacks permission."""

    status_code = 403


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    status_code = 404


class ConflictError(AppError):
    """Raised when an operation conflicts with existing state."""

    status_code = 409


class InternalServerError(AppError):
    """Represents an unexpected internal application error."""

    status_code = 500


# ---------------------------------------------------------------------------
# Product errors
# ---------------------------------------------------------------------------


class ProductNotFoundError(NotFoundError):
    def __init__(self, product_id: UUID) -> None:
        super().__init__(
            "Product not found",
            code="PRODUCT_NOT_FOUND",
        )
        self.product_id = product_id


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


# ---------------------------------------------------------------------------
# Brand errors
# ---------------------------------------------------------------------------


class BrandNotFoundError(NotFoundError):
    def __init__(self, brand_id: UUID) -> None:
        super().__init__(
            "Brand not found",
            code="BRAND_NOT_FOUND",
        )
        self.brand_id = brand_id


class BrandSlugAlreadyExistsError(ConflictError):
    def __init__(self, slug: str) -> None:
        super().__init__(
            "Brand slug already exists",
            code="BRAND_SLUG_ALREADY_EXISTS",
        )
        self.slug = slug


class BrandHasCollectionsError(ConflictError):
    def __init__(self, brand_id: UUID) -> None:
        super().__init__(
            "Brand cannot be deleted because it has associated collections",
            code="BRAND_HAS_COLLECTIONS",
        )
        self.brand_id = brand_id


# ---------------------------------------------------------------------------
# Collection errors
# ---------------------------------------------------------------------------


class CollectionNotFoundError(NotFoundError):
    def __init__(self, collection_id: UUID) -> None:
        super().__init__(
            "Collection not found",
            code="COLLECTION_NOT_FOUND",
        )
        self.collection_id = collection_id


class CollectionSlugAlreadyExistsError(ConflictError):
    def __init__(self, slug: str) -> None:
        super().__init__(
            "Collection slug already exists",
            code="COLLECTION_SLUG_ALREADY_EXISTS",
        )
        self.slug = slug
