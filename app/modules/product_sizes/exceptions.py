from uuid import UUID

from app.core.errors.base import NotFoundError, ValidationError


class ProductSizeNotFoundError(NotFoundError):
    def __init__(self, size_id: UUID) -> None:
        super().__init__(
            message=f"Product size not found: {size_id}",
            code="PRODUCT_SIZE_NOT_FOUND",
            details={
                "size_id": str(size_id),
            },
        )


class SizeMeasurementNotFoundError(NotFoundError):
    def __init__(self, measurement_id: UUID) -> None:
        super().__init__(
            message=f"Size measurement not found: {measurement_id}",
            code="SIZE_MEASUREMENT_NOT_FOUND",
            details={
                "measurement_id": str(measurement_id),
            },
        )


from uuid import UUID

from app.core.errors.base import NotFoundError


class ProductMeasurementGuideNotFoundError(NotFoundError):
    def __init__(self, guide_id: UUID) -> None:
        super().__init__(
            message=f"Product measurement guide not found: {guide_id}",
            code="PRODUCT_MEASUREMENT_GUIDE_NOT_FOUND",
            details={
                "guide_id": str(guide_id),
            },
        )


class ProductMeasurementGuideNotFoundForProductError(NotFoundError):
    def __init__(self, product_id: UUID) -> None:
        super().__init__(
            message=(f"Product measurement guide not found for product: {product_id}"),
            code="PRODUCT_MEASUREMENT_GUIDE_NOT_FOUND_FOR_PRODUCT",
            details={
                "product_id": str(product_id),
            },
        )


class ProductMeasurementGuideCannotBeNullError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            "Product measurement guide cannot be null",
            code="PRODUCT_MEASUREMENT_GUIDE_CANNOT_BE_NULL",
        )
