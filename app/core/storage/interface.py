from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.core.storage.types import ObjectMetadata


class AbstractObjectStorage(ABC):
    @abstractmethod
    async def create_object(
        self,
        *,
        storage_key: str,
        data: AsyncIterator[bytes],
        mime_type: str,
    ) -> None:
        """
        Create a new object in storage.
        """
        ...

    @abstractmethod
    async def upload_object(
        self,
        *,
        storage_key: str,
        data: AsyncIterator[bytes],
        mime_type: str,
    ) -> None:
        """
        Upload an object to storage.

        The object may already exist depending on
        provider semantics.
        """
        ...

    @abstractmethod
    async def update_object(
        self,
        *,
        storage_key: str,
        data: AsyncIterator[bytes],
        mime_type: str,
    ) -> None:
        """
        Replace/update an existing object.
        """
        ...

    @abstractmethod
    async def get_object(
        self,
        *,
        storage_key: str,
    ) -> bytes:
        """
        Retrieve the object's contents.
        """
        ...

    @abstractmethod
    async def get_object_metadata(
        self,
        *,
        storage_key: str,
    ) -> AsyncIterator[bytes]:
        """
        Retrieve metadata for an object.
        """
        ...

    @abstractmethod
    async def delete_object(
        self,
        *,
        storage_key: str,
    ) -> None:
        """
        Delete an object.
        """
        ...

    @abstractmethod
    async def create_presigned_upload_url(
        self,
        *,
        storage_key: str,
        mime_type: str,
        expires_in: int,
    ) -> str:
        """
        Create a temporary URL for direct client upload.
        """
        ...
