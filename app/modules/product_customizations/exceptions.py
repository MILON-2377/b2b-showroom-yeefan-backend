from uuid import UUID

from app.core.errors.base import NotFoundError, ValidationError


class ProductCustomizationNotFoundError(NotFoundError):
    def __init__(self, customization_id: UUID) -> None:
        super().__init__(
            message=f"Product customization not found: {customization_id}",
            code="PRODUCT_CUSTOMIZATION_NOT_FOUND",
            details={
                "customization_id": str(customization_id),
            },
        )


class ProductCustomizationNotFoundForProductError(NotFoundError):
    def __init__(self, product_id: UUID) -> None:
        super().__init__(
            message=(f"Product customization not found for product: {product_id}"),
            code="PRODUCT_CUSTOMIZATION_NOT_FOUND_FOR_PRODUCT",
            details={
                "product_id": str(product_id),
            },
        )


class ProductCustomizationOptionNotFoundError(NotFoundError):
    def __init__(self, option_id: UUID) -> None:
        super().__init__(
            message=f"Product customization option not found: {option_id}",
            code="PRODUCT_CUSTOMIZATION_OPTION_NOT_FOUND",
            details={
                "option_id": str(option_id),
            },
        )


class ProductCustomizationCannotBeNullError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            "Product customization cannot be null",
            code="PRODUCT_CUSTOMIZATION_CANNOT_BE_NULL",
        )
