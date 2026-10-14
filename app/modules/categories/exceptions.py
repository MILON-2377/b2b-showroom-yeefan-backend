from uuid import UUID

from app.core.errors.base import ConflictError, NotFoundError, ValidationError


class CategoryNotFoundError(NotFoundError):
    def __init__(self, category_id: UUID):
        super().__init__(
            code="CATEGORY_NOT_FOUND",
            message=f"Category '{category_id}' not found",
        )


class CategorySlugAlreadyExistsError(ConflictError):
    def __init__(self, slug: str):
        super().__init__(
            code="CATEGORY_SLUG_ALREADY_EXISTS",
            message=f"Category slug '{slug}' already exists",
        )



class CategoryBrandMismatchError(ValidationError):
    def __init__(
        self,
        *,
        category_id: UUID,
        brand_id: UUID,
    ) -> None:
        super().__init__(
            "Category does not belong to the specified brand",
            code="CATEGORY_BRAND_MISMATCH",
        )
        self.category_id = category_id
        self.brand_id = brand_id