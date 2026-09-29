from uuid import UUID

from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.models import RecordStatus
from app.modules.categories.model import Category
from app.shared.utils.slug import create_slug


class CategoryService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create(
        self,
        *,
        name: str,
        description: str | None = None,
        status: RecordStatus = RecordStatus.DRAFT,
    ) -> Category:
        slug = create_slug(name)

        if await self.uow.categories.exists_by_slug(slug):
            raise ValueError(f"Category slug '{slug}' already exists")

        category = Category(
            name=name,
            slug=slug,
            description=description,
            status=status,
        )

        await self.uow.categories.add(category)
        await self.uow.commit()

        return category

    async def get_by_id(
        self,
        category_id: UUID,
    ) -> Category | None:
        return await self.uow.categories.get_by_id(category_id)

    async def get_by_slug(
        self,
        slug: str,
    ) -> Category | None:
        return await self.uow.categories.get_by_slug(slug)

    async def list(
        self,
        *,
        status: RecordStatus | None = None,
    ) -> list[Category]:
        return await self.uow.categories.list(status=status)

    async def delete(
        self,
        category_id: UUID,
    ) -> None:
        category = await self.uow.categories.get_by_id(category_id)

        if category is None:
            raise ValueError(f"Category '{category_id}' not found")

        await self.uow.categories.delete(category)
        await self.uow.commit()
