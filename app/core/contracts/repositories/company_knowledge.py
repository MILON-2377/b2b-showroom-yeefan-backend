from abc import ABC, abstractmethod
from uuid import UUID

from app.core.models import RecordStatus
from app.modules.company_knowledge.model import (
    CompanyKnowledge,
)


class AbstractCompanyKnowledgeRepository(ABC):

    @abstractmethod
    async def update(
        self,
        knowledge: CompanyKnowledge,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        knowledge: CompanyKnowledge,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        knowledge_id: UUID,
    ) -> CompanyKnowledge | None:
        raise NotImplementedError

    @abstractmethod
    async def list_admin(
        self,
        *,
        page: int,
        page_size: int,
        search: str | None = None,
        status: RecordStatus | None = None,
    ) -> tuple[list[CompanyKnowledge], int]:
        raise NotImplementedError

    @abstractmethod
    async def search_published(
        self,
        *,
        query: str,
        limit: int = 5,
    ) -> list[CompanyKnowledge]:
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        knowledge: CompanyKnowledge,
    ) -> None:
        raise NotImplementedError
