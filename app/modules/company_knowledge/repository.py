from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.contracts.repositories.company_knowledge import (
    AbstractCompanyKnowledgeRepository,
)
from app.core.models import RecordStatus
from app.modules.company_knowledge.model import (
    CompanyKnowledge,
)


class CompanyKnowledgeRepository(AbstractCompanyKnowledgeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def update(self,  knowledge: CompanyKnowledge) -> CompanyKnowledge:
        self.session.add(knowledge)
        await self.session.flush()
        return knowledge

    async def create(self, knowledge: CompanyKnowledge) -> None:
        self.session.add(knowledge)

    async def get_by_id(
        self,
        knowledge_id: UUID,
    ) -> CompanyKnowledge | None:
        statement = select(CompanyKnowledge).where(CompanyKnowledge.id == knowledge_id)

        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> tuple[list[CompanyKnowledge], int]:
        filters = []

        if search:
            pattern = f"%{search.strip()}%"
            filters.append(
                or_(
                    CompanyKnowledge.title.ilike(pattern),
                    CompanyKnowledge.category.ilike(pattern),
                    CompanyKnowledge.content.ilike(pattern),
                )
            )

        if status is not None:
            filters.append(CompanyKnowledge.status == status)

        count_statement = (
            select(func.count()).select_from(CompanyKnowledge).where(*filters)
        )
        total_result = await self.session.execute(count_statement)
        total = total_result.scalar_one()

        statement = (
            select(CompanyKnowledge)
            .where(*filters)
            .order_by(
                CompanyKnowledge.created_at.desc(),
                CompanyKnowledge.id.asc(),
            )
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.session.execute(statement)

        return list(result.scalars().all()), total

    async def search_published(
        self,
        *,
        query: str,
        limit: int = 5,
    ) -> list[CompanyKnowledge]:
        search_query = query.strip()

        if not search_query:
            return []

        pattern = f"%{search_query}%"

        statement = (
            select(CompanyKnowledge)
            .where(
                CompanyKnowledge.status == RecordStatus.PUBLISHED,
                or_(
                    CompanyKnowledge.title.ilike(pattern),
                    CompanyKnowledge.category.ilike(pattern),
                    CompanyKnowledge.content.ilike(pattern),
                ),
            )
            .order_by(
                CompanyKnowledge.updated_at.desc(),
                CompanyKnowledge.created_at.desc(),
            )
            .limit(limit)
        )

        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def delete(self, knowledge: CompanyKnowledge) -> None:
        await self.session.delete(knowledge)
