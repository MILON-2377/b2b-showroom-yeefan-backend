from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.auth.models.user import UserRole


@dataclass(frozen=True)
class UserDTO:
    id: UUID
    email: str
    role: UserRole | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class UserListDTO:
    items: list[UserDTO]
    page: int
    page_size: int
    total: int
