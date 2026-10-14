from app.core.errors.base import NotFoundError


class BrandNotFoundError(NotFoundError):
    def __init__(self, brand_id):
        self.brand_id = brand_id
        super().__init__(f"Brand not found: {brand_id}")
