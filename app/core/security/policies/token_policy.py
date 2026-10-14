from datetime import datetime, timedelta, timezone

from app.core.config import Settings


class TokenPolicy:
    def __init__(self, security_settings: Settings) -> None:
        self.security_settings = security_settings

    def access_token_expires_at(
        self,
        *,
        issued_at: datetime | None = None,
    ) -> datetime:
        issued_at = issued_at or datetime.now(timezone.utc)

        return issued_at + timedelta(
            minutes=self.security_settings.access_token_expire_minutes,
        )

    def refresh_token_expires_at(
        self,
        *,
        issued_at: datetime | None = None,
    ) -> datetime:
        issued_at = issued_at or datetime.now(timezone.utc)

        return issued_at + timedelta(
            days=self.security_settings.refresh_token_expire_days,
        )
