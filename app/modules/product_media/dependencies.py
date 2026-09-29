from collections.abc import AsyncGenerator

from fastapi import Depends

from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.storage.dependencies import get_object_storage
from app.core.storage.interface import AbstractObjectStorage
from app.modules.product_media.service import ProductMediaService
from app.shared.dependencies import get_uow


async def get_product_media_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    storage: AbstractObjectStorage = Depends(get_object_storage),
) -> ProductMediaService:
    return ProductMediaService(
        uow=uow,
        storage=storage,
    )
