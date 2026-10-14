from uuid import UUID

from app.core.errors.base import ConflictError, NotFoundError, ValidationError


class MultiplePrimaryProductMediaError(ConflictError):
    def __init__(self) -> None:
        super().__init__(
            "A product can have only one primary media",
            code="MULTIPLE_PRIMARY_PRODUCT_MEDIA",
        )


class ProductMediaNotFoundError(NotFoundError):
    def __init__(self, product_media_id: UUID) -> None:
        super().__init__(
            message=f"Product media not found: {product_media_id}",
            code="PRODUCT_MEDIA_NOT_FOUND",
            details={
                "product_media_id": str(product_media_id),
            },
        )


class DuplicateProductMediaError(ValidationError):
    def __init__(self, media_asset_id: UUID) -> None:
        super().__init__(
            "The same media asset cannot be added to a product more than once",
            code="DUPLICATE_PRODUCT_MEDIA",
        )
        self.media_asset_id = media_asset_id
