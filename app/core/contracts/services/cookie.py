from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import Request, Response


class AbstractCookieService(ABC):
    @abstractmethod
    def set_auth_cookies(
        self,
        response: Response,
        *,
        access_token: str,
        refresh_token: str,
        access_token_expires_at: datetime,
    ) -> None: ...

    @abstractmethod
    def get_access_token(
        self,
        request: Request,
    ) -> str | None: ...

    @abstractmethod
    def get_refresh_token(
        self,
        request: Request,
    ) -> str | None: ...

    @abstractmethod
    def clear_auth_cookies(
        self,
        response: Response,
    ) -> None: ...
