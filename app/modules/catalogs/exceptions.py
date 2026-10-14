from uuid import UUID

from app.core.errors.base import ConflictError, NotFoundError, ValidationError


class CatalogNotFoundError(NotFoundError):
    def __init__(self, catalog_id: UUID) -> None:
        super().__init__(
            message=f"Catalog '{catalog_id}' was not found.",
            code="CATALOG_NOT_FOUND",
        )


class InvalidCatalogMediaError(ValidationError):
    def __init__(self, media_asset_id: UUID) -> None:
        super().__init__(
            message=(f"Media asset '{media_asset_id}' is not a valid catalog PDF."),
            code="INVALID_CATALOG_MEDIA",
        )





class CatalogAlreadyExistsError(ConflictError):
    def __init__(self, collection_id: UUID) -> None:
        super().__init__(
            message=f"A catalog already exists for collection '{collection_id}'.",
            code="CATALOG_ALREADY_EXISTS",
        )