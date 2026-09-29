from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.categories.model import Category


class AbstractCategoryRepository(ABC):
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
        *,
        status: RecordStatus | None = None,
    ) -> list[Category]: ...

    @abstractmethod
    async def exists_by_slug(
        self,
        slug: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool: ...

    @abstractmethod
    async def add(
        self,
        category: Category,
    ) -> Category: ...

    @abstractmethod
    async def delete(
        self,
        category: Category,
    ) -> None: ...
