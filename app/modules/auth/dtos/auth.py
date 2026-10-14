from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.auth.models.user import User


@dataclass(frozen=True)
class AuthenticatedUser:
    user: User
    session_id: UUID


@dataclass(frozen=True)
class AuthTokensDTO:
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime
    session_id: UUID


@dataclass(frozen=True)
class LoginDTO:
    email: str
    password: str
    device_name: str | None = None
    user_agent: str | None = None
    ip_address: str | None = None


@dataclass(frozen=True)
class AccessTokenDTO:
    token: str
    expires_at: datetime
