from fastapi import Depends

from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.company_knowledge.service import CompanyKnowledgeService
from app.shared.dependencies import get_uow


def get_company_knowledge_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> CompanyKnowledgeService:
    return CompanyKnowledgeService(uow)
