from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionResponse(BaseModel):
    id: UUID
    device_name: str | None
    user_agent: str | None
    ip_address: str | None
    created_at: datetime
    last_active_at: datetime
    expires_at: datetime
    revoked_at: datetime | None
