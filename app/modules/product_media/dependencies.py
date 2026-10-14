from fastapi import Depends

from app.core.contracts.services.media_upload import AbstractMediaUploadService
from app.core.contracts.services.product_media import (
    AbstractProductMediaService,
)
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.modules.media.dependencies import get_media_upload_service
from app.modules.product_media.service import (
    ProductMediaService,
)
from app.shared.dependencies import get_uow


def get_product_media_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    upload_media_service: AbstractMediaUploadService = Depends(
        get_media_upload_service
    ),
) -> AbstractProductMediaService:
    return ProductMediaService(uow=uow, upload_media_service=upload_media_service)
