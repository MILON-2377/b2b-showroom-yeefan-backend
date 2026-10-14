from abc import ABC, abstractmethod
from uuid import UUID

from app.core.database.models import Brand
from app.core.models import RecordStatus
from app.modules.brands.dtos import (
    BrandDTO,
    PublicBrandListDTO,
    PublicBrandQueryDTO,
)


class AbstractBrandService(ABC):
    @abstractmethod
    async def list_public(
        self,
        query: PublicBrandQueryDTO,
    ) -> PublicBrandListDTO:
        raise NotImplementedError

    @abstractmethod
    async def validate_for_product(
        self,
        *,
        brand_id: UUID,
    ) -> BrandDTO: ...

    @abstractmethod
    async def create(
        self,
        *,
        name: str,
        description: str | None = None,
        logo_media_url: str | None = None,
    ) -> Brand: ...

    @abstractmethod
    async def get_by_id(
        self,
        brand_id: UUID,
    ) -> Brand: ...

    @abstractmethod
    async def list(
        self,
        *,
        status: RecordStatus | None = None,
    ) -> list[Brand]: ...

    @abstractmethod
    async def delete(
        self,
        brand_id: UUID,
    ) -> None: ...

    @abstractmethod
    async def update(
        self,
        brand_id: UUID,
        name: str,
        description: str | None = None,
        status: RecordStatus | None = None,
    ) -> Brand: ...
