from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class SessionDTO:
    id: UUID
    device_name: str | None
    user_agent: str | None
    ip_address: str | None
    created_at: datetime
    last_active_at: datetime
    expires_at: datetime
    revoked_at: datetime | None


