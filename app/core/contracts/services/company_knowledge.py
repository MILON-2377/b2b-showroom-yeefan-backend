from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.company_knowledge.dtos import (
    CompanyKnowledgeDTO,
    CreateCompanyKnowledgeDTO,
    UpdateCompanyKnowledgeDTO,
)


class AbstractCompanyKnowledgeService(ABC):
    @abstractmethod
    async def create(
        self,
        data: CreateCompanyKnowledgeDTO,
    ) -> CompanyKnowledgeDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        knowledge_id: UUID,
    ) -> CompanyKnowledgeDTO:
        raise NotImplementedError

    @abstractmethod
    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> tuple[list[CompanyKnowledgeDTO], int]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        knowledge_id: UUID,
        data: UpdateCompanyKnowledgeDTO,
    ) -> CompanyKnowledgeDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        knowledge_id: UUID,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search_published(
        self,
        *,
        query: str,
        limit: int = 5,
    ) -> list[CompanyKnowledgeDTO]:
        raise NotImplementedError
