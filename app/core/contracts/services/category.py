from abc import ABC, abstractmethod
from uuid import UUID

from app.core.database.models import Category
from app.core.models import RecordStatus
from app.modules.categories.dtos import (
    CategoryDTO,
    CategoryListItem,
    CreateCategoryDTO,
    PublicCategoryListDTO,
    UpdateCategoryDTO,
)
from app.modules.categories.query import CategoryListResult


class AbstractCategoryService(ABC):
    @abstractmethod
    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
    ) -> PublicCategoryListDTO:
        raise NotImplementedError

    @abstractmethod
    async def validate_for_product(
        self,
        *,
        category_id: UUID,
        brand_id: UUID,
    ) -> CategoryDTO: ...

    @abstractmethod
    async def create(
        self,
        *,
        payload: CreateCategoryDTO,
    ) -> CategoryListItem: ...

    @abstractmethod
    async def get_by_id(
        self,
        category_id: UUID,
    ) -> Category | None: ...

    @abstractmethod
    async def get_by_slug(
        self,
        slug: str,
    ) -> Category | None: ...

    @abstractmethod
    async def list(
        self,
        search: str | None = None,
        status: RecordStatus | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> CategoryListResult: ...

    @abstractmethod
    async def update(
        self,
        *,
        category_id: UUID,
        payload: UpdateCategoryDTO,
    ) -> CategoryListItem: ...

    @abstractmethod
    async def delete(
        self,
        category_id: UUID,
    ) -> None: ...
