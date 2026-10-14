from dataclasses import dataclass
from uuid import UUID

from app.modules.auth.models.user import User


@dataclass(frozen=True)
class AuthContext:
    user: User
    session_id: UUID
