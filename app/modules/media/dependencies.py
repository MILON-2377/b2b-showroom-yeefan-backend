from fastapi import Depends

from app.core.contracts.storage.media import AbstractMediaStorage
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.storage.dependencies import get_media_storage
from app.modules.media.service import MediaUploadService
from app.shared.dependencies import get_uow


def get_media_upload_service(
    uow: AbstractUnitOfWork = Depends(get_uow),
    storage: AbstractMediaStorage = Depends(get_media_storage),
) -> MediaUploadService:
    return MediaUploadService(
        uow=uow,
        storage=storage,
    )
