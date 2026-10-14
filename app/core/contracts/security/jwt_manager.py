from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class AbstractJwtManager(ABC):
    @abstractmethod
    def create_access_token(
        self,
        *,
        subject: str,
        session_id: UUID,
        expires_at,
    ) -> str: ...

    @abstractmethod
    def decode_access_token(
        self,
        token: str,
    ) -> dict[str, Any] | None: ...
