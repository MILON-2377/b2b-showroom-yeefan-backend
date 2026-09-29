from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.brands.model import Brand


class AbstractBrandRepository(ABC):
    @abstractmethod
    async def get_by_id(self, brand_id: UUID) -> Brand | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Brand | None: ...

    @abstractmethod
    async def list(
        self,
        *,
        status: RecordStatus | None = None,
    ) -> list[Brand]: ...

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
