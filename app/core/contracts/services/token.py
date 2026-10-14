from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from uuid import UUID

from app.modules.auth.dtos.auth import AccessTokenDTO


class AbstractTokenService(ABC):
    @abstractmethod
    def create_access_token(
        self,
        subject: str,
        session_id: UUID
    ) -> AccessTokenDTO: ...

    @abstractmethod
    def decode_access_token(
        self,
        token: str,
    ) -> dict[str, Any] | None: ...

    @abstractmethod
    def generate_refresh_token(self) -> str: ...

    @abstractmethod
    def hash_refresh_token(self, token: str) -> str: ...

    @abstractmethod
    def refresh_token_expires_at(
        self,
        issued_at: datetime,
    ) -> datetime: ...
