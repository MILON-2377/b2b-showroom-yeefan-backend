from uuid import UUID

from app.core.errors.base import (
    ConflictError,
    NotFoundError,
    ValidationError,
)


class CollectionNotFoundError(NotFoundError):
    def __init__(self, collection_id: UUID) -> None:
        super().__init__(
            message=f"Collection not found: {collection_id}",
            code="COLLECTION_NOT_FOUND",
        )
        self.collection_id = collection_id


class CollectionSlugAlreadyExistsError(ConflictError):
    def __init__(self, slug: str) -> None:
        super().__init__(
            message="Collection slug already exists",
            code="COLLECTION_SLUG_ALREADY_EXISTS",
        )
        self.slug = slug


class CollectionBrandMismatchError(ValidationError):
    def __init__(
        self,
        *,
        collection_id: UUID,
        brand_id: UUID,
    ) -> None:
        super().__init__(
            message=(f"Collection {collection_id} does not belong to brand {brand_id}"),
            code="COLLECTION_BRAND_MISMATCH",
        )
        self.collection_id = collection_id
        self.brand_id = brand_id
