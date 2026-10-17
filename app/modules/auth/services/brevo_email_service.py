import logging

import httpx

from app.core.config import settings
from app.core.contracts.services.email_service import (
    AbstractEmailService,
)

logger = logging.getLogger(__name__)


class BrevoEmailService(AbstractEmailService):
    API_URL = "https://api.brevo.com/v3/smtp/email"

    def __init__(self) -> None:
        self.api_key = settings.brevo_api_key
        self.sender_email = settings.brevo_sender_email
        self.sender_name = settings.brevo_sender_name

    async def send_login_code(
        self,
        *,
        to_email: str,
        code: str,
    ) -> None:
        payload = {
            "sender": {
                "name": self.sender_name,
                "email": self.sender_email,
            },
            "to": [
                {
                    "email": to_email,
                }
            ],
            "subject": "Your YIFAN BRIDAL login verification code",
            "textContent": (
                f"Your login verification code is {code}.\n\n"
                "This code expires in 5 minutes. "
                "Do not share it with anyone.\n\n"
                "If you did not attempt to log in, you can ignore this email."
            ),
        }

        headers = {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    self.API_URL,
                    json=payload,
                    headers=headers,
                )

                response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            logger.error(
                "Brevo API request failed: status=%s, response=%s",
                exc.response.status_code,
                exc.response.text,
            )
            raise

        except httpx.RequestError:
            logger.exception("Failed to connect to Brevo email API")
            raise
