from fastapi import Depends

from app.core.contracts.services.catalog import AbstractCatalogService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.catalogs.service import CatalogService
from app.shared.dependencies import get_uow


def get_catalog_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractCatalogService:
    return CatalogService(uow=uow)
