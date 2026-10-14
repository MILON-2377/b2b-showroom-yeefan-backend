from fastapi import Depends

from app.core.contracts.services.product_color import AbstractProductColorService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.product_colors.service import ProductColorService
from app.shared.dependencies import get_uow


def get_product_color_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
) -> AbstractProductColorService:
    return ProductColorService(uow=uow)
