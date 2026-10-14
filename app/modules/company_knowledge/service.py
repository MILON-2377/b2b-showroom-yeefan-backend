from uuid import UUID

from app.core.contracts.services.company_knowledge import (
    AbstractCompanyKnowledgeService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.models import RecordStatus
from app.modules.company_knowledge.dtos import (
    CompanyKnowledgeDTO,
    CreateCompanyKnowledgeDTO,
    UpdateCompanyKnowledgeDTO,
)
from app.modules.company_knowledge.exceptions import CompanyKnowledgeNotFoundError
from app.modules.company_knowledge.model import (
    CompanyKnowledge,
)


class CompanyKnowledgeService(AbstractCompanyKnowledgeService):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def create(
        self,
        data: CreateCompanyKnowledgeDTO,
    ) -> CompanyKnowledgeDTO:

        knowledge = CompanyKnowledge(
            title=data.title.strip(),
            category=data.category.strip(),
            content=data.content.strip(),
            status=RecordStatus.DRAFT,
        )

        await self.uow.company_knowledges.create(knowledge)
        await self.uow.commit()
        return CompanyKnowledgeDTO.model_validate(knowledge)

    async def get_by_id(
        self,
        knowledge_id: UUID,
    ) -> CompanyKnowledgeDTO:

        knowledge = await self.uow.company_knowledges.get_by_id(knowledge_id)

        if knowledge is None:
            raise CompanyKnowledgeNotFoundError("Company knowledge not found")

        return CompanyKnowledgeDTO.model_validate(knowledge)

    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> tuple[list[CompanyKnowledgeDTO], int]:

        items, total = await self.uow.company_knowledges.list_admin(
            page=page,
            page_size=page_size,
            search=search,
            status=status,
        )

        return (
            [CompanyKnowledgeDTO.model_validate(item) for item in items],
            total,
        )

    async def update(
        self,
        knowledge_id: UUID,
        data: UpdateCompanyKnowledgeDTO,
    ) -> CompanyKnowledgeDTO:

        knowledge = await self.uow.company_knowledges.get_by_id(knowledge_id)

        if knowledge is None:
            raise CompanyKnowledgeNotFoundError("Company knowledge not found")

        updates = data.model_dump(exclude_unset=True)

        for field, value in updates.items():
            if value is not None and isinstance(value, str):
                value = value.strip()
            setattr(knowledge, field, value)

        await self.uow.commit()

        return CompanyKnowledgeDTO.model_validate(knowledge)

    async def delete(self, knowledge_id: UUID) -> None:

        knowledge = await self.uow.company_knowledges.get_by_id(knowledge_id)

        if knowledge is None:
            raise CompanyKnowledgeNotFoundError("Company knowledge not found")

        await self.uow.company_knowledges.delete(knowledge)
        await self.uow.commit()

    async def search_published(
        self,
        *,
        query: str,
        limit: int = 5,
    ) -> list[CompanyKnowledgeDTO]:

        items = await self.uow.company_knowledges.search_published(
            query=query,
            limit=limit,
        )

        return [CompanyKnowledgeDTO.model_validate(item) for item in items]
