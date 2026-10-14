from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.brands.model import Brand
from app.modules.brands.query import BrandListQuery, BrandListResult


class AbstractBrandRepository(ABC):
    @abstractmethod
    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
    ) -> tuple[list[Brand], int]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, brand_id: UUID) -> Brand | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Brand | None: ...

    @abstractmethod
    async def list(self, query: BrandListQuery) -> BrandListResult: ...

    @abstractmethod
    async def exists_by_slug(
        self,
        slug: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool: ...

    @abstractmethod
    async def add(self, brand: Brand) -> Brand: ...

    @abstractmethod
    async def delete(self, brand: Brand) -> None: ...

    @abstractmethod
    async def update(self, brand: Brand) -> Brand: ...
