from collections.abc import AsyncIterator
from pathlib import Path

from app.core.storage.interface import AbstractObjectStorage
from app.core.storage.types import ObjectMetadata


class LocalObjectStorage(AbstractObjectStorage):
    def __init__(self, root_path: Path):
        self.root_path = root_path

    def _resolve_path(self, storage_key: str) -> Path:
        return self.root_path / storage_key

    async def create_object(
        self,
        *,
        storage_key: str,
        data: AsyncIterator[bytes],
        mime_type: str,
    ) -> None:
        path = self._resolve_path(storage_key)

        if path.exists():
            raise FileExistsError(f"Object already exists: {storage_key}")

        await self._write_object(
            path=path,
            data=data,
        )

    async def upload_object(
        self,
        *,
        storage_key: str,
        data: AsyncIterator[bytes],
        mime_type: str,
    ) -> None:
        path = self._resolve_path(storage_key)

        await self._write_object(
            path=path,
            data=data,
        )

    async def update_object(
        self,
        *,
        storage_key: str,
        data: AsyncIterator[bytes],
        mime_type: str,
    ) -> None:
        path = self._resolve_path(storage_key)

        if not path.is_file():
            raise FileNotFoundError(f"Object does not exist: {storage_key}")

        await self._write_object(
            path=path,
            data=data,
        )

    async def get_object(
        self,
        *,
        storage_key: str,
    ) -> AsyncIterator[bytes]:
        path = self._resolve_path(storage_key)

        if not path.is_file():
            raise FileNotFoundError(f"Object does not exist: {storage_key}")

        with path.open("rb") as file:
            while chunk := file.read(1024 * 1024):
                yield chunk

    async def get_object_metadata(
        self,
        *,
        storage_key: str,
    ) -> ObjectMetadata | None:
        path = self._resolve_path(storage_key)

        if not path.is_file():
            return None

        return ObjectMetadata(
            storage_key=storage_key,
            mime_type="application/octet-stream",
            size=path.stat().st_size,
        )

    async def delete_object(
        self,
        *,
        storage_key: str,
    ) -> None:
        path = self._resolve_path(storage_key)

        if path.is_file():
            path.unlink()

    async def create_presigned_upload_url(
        self,
        *,
        storage_key: str,
        mime_type: str,
        expires_in: int,
    ) -> str:
        path = self._resolve_path(storage_key)
        path.parent.mkdir(parents=True, exist_ok=True)

        return f"/local-storage/upload/{storage_key}"

    async def _write_object(
        self,
        *,
        path: Path,
        data: AsyncIterator[bytes],
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("wb") as file:
            async for chunk in data:
                file.write(chunk)
