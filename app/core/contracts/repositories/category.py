from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.categories.model import Category
from app.modules.categories.query import CategoryListQuery, CategoryListResult


class AbstractCategoryRepository(ABC):

    @abstractmethod
    async def list_public(
        self,
        *,
        page: int,
        page_size: int
    ) -> CategoryListResult:
        raise NotImplementedError

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
    async def list(self, query: CategoryListQuery) -> CategoryListResult: ...

    @abstractmethod
    async def exists_by_slug(
        self,
        slug: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool: ...

    @abstractmethod
    async def create(
        self,
        category: Category,
    ) -> Category: ...

    @abstractmethod
    async def update(self, category: Category) -> Category: ...

    @abstractmethod
    async def delete(
        self,
        category: Category,
    ) -> None: ...
