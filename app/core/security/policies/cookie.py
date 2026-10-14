from typing import TypedDict

from app.core.config import Settings


class CookieOptions(TypedDict):
    key: str
    httponly: bool
    secure: bool
    samesite: str
    path: str


class CookiePolicy:
    def __init__(self, cookie_settings: Settings) -> None:
        self.cookie_settings = cookie_settings

    def access_cookie_kwargs(self) -> CookieOptions:
        return {
            "key": self.cookie_settings.access_token_cookie_name,
            "httponly": self.cookie_settings.auth_cookie_httponly,
            "secure": self.cookie_settings.auth_cookie_secure,
            "samesite": self.cookie_settings.auth_cookie_samesite,
            "path": self.cookie_settings.access_token_cookie_path,
        }

    def refresh_cookie_kwargs(self) -> CookieOptions:
        return {
            "key": self.cookie_settings.refresh_token_cookie_name,
            "httponly": self.cookie_settings.auth_cookie_httponly,
            "secure": self.cookie_settings.auth_cookie_secure,
            "samesite": self.cookie_settings.auth_cookie_samesite,
            "path": self.cookie_settings.refresh_token_cookie_path,
        }

    @property
    def access_token_name(self) -> str:
        return self.cookie_settings.access_token_cookie_name

    @property
    def refresh_token_name(self) -> str:
        return self.cookie_settings.refresh_token_cookie_name

    @property
    def access_token_path(self) -> str:
        return self.cookie_settings.access_token_cookie_path

    @property
    def refresh_token_path(self) -> str:
        return self.cookie_settings.refresh_token_cookie_path
