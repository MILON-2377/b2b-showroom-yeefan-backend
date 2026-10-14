from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.contracts.repositories.category import (
    AbstractCategoryRepository,
)
from app.core.models import RecordStatus
from app.modules.categories.model import Category

from .query import CategoryListQuery, CategoryListResult


class CategoryRepository(AbstractCategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        category_id: UUID,
    ) -> Category | None:
        statement = (
            select(Category)
            .options(selectinload(Category.image_media))
            .where(Category.id == category_id)
        )

        result = await self.session.execute(statement)

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
        query: CategoryListQuery,
    ) -> CategoryListResult:
        filters = []

        if query.search:
            search = f"%{query.search}%"

            filters.append(
                or_(
                    Category.name.ilike(search),
                    Category.slug.ilike(search),
                )
            )

        if query.status is not None:
            filters.append(Category.status == query.status)

        count_statement = select(func.count()).select_from(Category).where(*filters)

        total = await self.session.scalar(count_statement)

        statement = (
            select(Category)
            .options(selectinload(Category.image_media))
            .where(*filters)
            .order_by(Category.created_at.desc())
            .offset((query.page - 1) * query.page_size)
            .limit(query.page_size)
        )

        result = await self.session.scalars(statement)

        return CategoryListResult(
            items=list(result),
            total=total or 0,
        )

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

    async def create(
        self,
        category: Category,
    ) -> Category:
        self.session.add(category)
        return category

    async def update(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.flush()
        await self.session.refresh(category)
        return category

    async def delete(
        self,
        category: Category,
    ) -> None:
        await self.session.delete(category)

    async def list_public(
        self,
        *,
        page: int,
        page_size: int,
    ) -> CategoryListResult:
        filters = [
            Category.status == RecordStatus.PUBLISHED,
        ]

        count_statement = select(func.count()).select_from(Category).where(*filters)

        total = await self.session.scalar(count_statement)

        statement = (
            select(Category)
            .options(
                selectinload(Category.image_media),
            )
            .where(*filters)
            .order_by(Category.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.session.scalars(statement)

        return CategoryListResult(
            items=list(result),
            total=total or 0,
        )
