from datetime import datetime, timedelta, timezone

from app.core.config import Settings


class SessionPolicy:
    def __init__(self, security_settings: Settings) -> None:
        self.security_settings = security_settings

    def calculate_expiration(
        self,
        *,
        created_at: datetime | None = None,
    ) -> datetime:
        created_at = created_at or datetime.now(timezone.utc)

        return created_at + timedelta(
            days=self.security_settings.session_expire_days,
        )
