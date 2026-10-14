from fastapi import Depends

from app.core.contracts.services.collection import AbstractCollectionService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.collections.service import CollectionService
from app.shared.dependencies import get_uow


def get_collection_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractCollectionService:
    return CollectionService(uow=uow)
