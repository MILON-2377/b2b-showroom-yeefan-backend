from datetime import datetime

from fastapi import Request, Response

from app.core.contracts.services.cookie import AbstractCookieService
from app.core.security.policies.cookie import CookiePolicy


class CookieService(AbstractCookieService):
    def __init__(self, cookie_policy: CookiePolicy) -> None:
        self.cookie_policy = cookie_policy

    def set_auth_cookies(
        self,
        response: Response,
        *,
        access_token: str,
        refresh_token: str,
        access_token_expires_at: datetime,
    ) -> None:
        access_kwargs = self.cookie_policy.access_cookie_kwargs()

        response.set_cookie(
            value=access_token,
            expires=access_token_expires_at,
            **access_kwargs,
        )

        refresh_kwargs = self.cookie_policy.refresh_cookie_kwargs()

        response.set_cookie(
            value=refresh_token,
            **refresh_kwargs,
        )

    def get_access_token(
        self,
        request: Request,
    ) -> str | None:
        return request.cookies.get(self.cookie_policy.access_token_name)

    def get_refresh_token(
        self,
        request: Request,
    ) -> str | None:
        return request.cookies.get(self.cookie_policy.refresh_token_name)

    def clear_auth_cookies(
        self,
        response: Response,
    ) -> None:
        response.delete_cookie(
            key=self.cookie_policy.access_token_name,
            path=self.cookie_policy.access_token_path,
        )

        response.delete_cookie(
            key=self.cookie_policy.refresh_token_name,
            path=self.cookie_policy.refresh_token_path,
        )
