from uuid import UUID

from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.models import RecordStatus
from app.modules.brands.model import Brand
from app.shared.utils.slug import create_slug


class BrandService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create(
        self,
        *,
        name: str,
        description: str | None = None,
        logo_media_url: str | None = None,
        status: RecordStatus = RecordStatus.DRAFT,
    ) -> Brand:

        slug = create_slug(name)

        if await self.uow.brands.exists_by_slug(slug):
            raise ValueError(f"Brand slug '{slug}' already exists")

        brand = Brand(
            name=name,
            slug=slug,
            description=description,
            logo_media_url=logo_media_url,
            status=status,
        )

        await self.uow.brands.add(brand)
        await self.uow.commit()

        return brand

    async def get_by_id(self, brand_id: UUID) -> Brand | None:
        return await self.uow.brands.get_by_id(brand_id)

    async def get_by_slug(self, slug: str) -> Brand | None:
        return await self.uow.brands.get_by_slug(slug)

    async def list(
        self,
        *,
        status: RecordStatus | None = None,
    ) -> list[Brand]:
        return await self.uow.brands.list(status=status)

    async def delete(self, brand_id: UUID) -> None:
        brand = await self.uow.brands.get_by_id(brand_id)

        if brand is None:
            raise ValueError(f"Brand '{brand_id}' not found")

        await self.uow.brands.delete(brand)
        await self.uow.commit()
