from collections.abc import AsyncGenerator

from app.core.config import settings
from app.core.contracts.storage.media import AbstractMediaStorage
from app.core.storage.cloudinary import CloudinaryMediaStorage
from app.core.storage.interface import AbstractObjectStorage
from app.core.storage.local import LocalObjectStorage


def get_media_storage() -> AbstractMediaStorage:
    return CloudinaryMediaStorage()


def get_media_storage() -> AbstractMediaStorage:
    return CloudinaryMediaStorage()


async def get_object_storage() -> AsyncGenerator[AbstractObjectStorage, None]:
    yield LocalObjectStorage(settings.storage_root)
