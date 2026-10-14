from fastapi import Depends

from app.core.contracts.services.brand import AbstractBrandService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.brands.service import BrandService
from app.shared.dependencies import get_uow


def get_brand_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractBrandService:
    return BrandService(uow=uow)
