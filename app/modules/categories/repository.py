from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.category import (
    AbstractCategoryRepository,
)
from app.core.models import RecordStatus
from app.modules.categories.model import Category


class CategoryRepository(AbstractCategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        category_id: UUID,
    ) -> Category | None:
        result = await self.session.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(
        self,
        slug: str,
    ) -> Category | None:
        result = await self.session.execute(
            select(Category).where(Category.slug == slug)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        *,
        status: RecordStatus | None = None,
    ) -> list[Category]:
        statement = select(Category).order_by(Category.name)

        if status is not None:
            statement = statement.where(Category.status == status)

        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def exists_by_slug(
        self,
        slug: str,
        *,
        exclude_id: UUID | None = None,
    ) -> bool:
        statement = select(Category.id).where(Category.slug == slug)

        if exclude_id is not None:
            statement = statement.where(Category.id != exclude_id)

        result = await self.session.execute(statement)

        return result.scalar_one_or_none() is not None

    async def add(
        self,
        category: Category,
    ) -> Category:
        self.session.add(category)
        return category

    async def delete(
        self,
        category: Category,
    ) -> None:
        await self.session.delete(category)
