import asyncio

from app.modules.auth.services.brevo_email_service import (
    BrevoEmailService,
)


async def main() -> None:
    service = BrevoEmailService()

    await service.send_login_code(
        to_email="YOUR_TEST_EMAIL@example.com",
        code="123456",
    )

    print("Brevo accepted the email request.")


if __name__ == "__main__":
    asyncio.run(main())