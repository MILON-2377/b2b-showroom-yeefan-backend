from collections.abc import AsyncGenerator

from app.core.config import settings
from app.core.storage.interface import AbstractObjectStorage
from app.core.storage.local import LocalObjectStorage


async def get_object_storage() -> AsyncGenerator[AbstractObjectStorage, None]:
    yield LocalObjectStorage(settings.storage_root)
