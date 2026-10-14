from app.core.errors.base import ConflictError, NotFoundError, ValidationError


class ReviewNotFoundError(NotFoundError):
    def __init__(self, review_id: str) -> None:
        super().__init__(
            message="Review not found.",
            code="REVIEW_NOT_FOUND",
            details={"review_id": review_id},
        )


class ReviewProductNotFoundError(ValidationError):
    def __init__(self, product_id: str) -> None:
        super().__init__(
            message="The specified product does not exist.",
            code="REVIEW_PRODUCT_NOT_FOUND",
            details={"product_id": product_id},
        )


class ReviewProductUnavailableError(ValidationError):
    def __init__(self, product_id: str) -> None:
        super().__init__(
            message="The specified product is not available for reviews.",
            code="REVIEW_PRODUCT_UNAVAILABLE",
            details={"product_id": product_id},
        )


class ReviewAvatarNotFoundError(ValidationError):
    def __init__(self, media_id: str) -> None:
        super().__init__(
            message="The specified avatar media asset does not exist.",
            code="REVIEW_AVATAR_NOT_FOUND",
            details={"media_id": media_id},
        )


class ReviewAvatarNotReadyError(ValidationError):
    def __init__(self, media_id: str) -> None:
        super().__init__(
            message="The specified avatar media asset is not ready.",
            code="REVIEW_AVATAR_NOT_READY",
            details={"media_id": media_id},
        )


class ReviewAlreadyApprovedError(ConflictError):
    def __init__(self, review_id: str) -> None:
        super().__init__(
            message="Review is already approved.",
            code="REVIEW_ALREADY_APPROVED",
            details={"review_id": review_id},
        )