
import asyncio

import httpx

from app.core.config import settings


async def main() -> None:
    headers = {
        "accept": "application/json",
        "api-key": settings.brevo_api_key,
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            "https://api.brevo.com/v3/account",
            headers=headers,
        )

        print("HTTP status:", response.status_code)
        print("Response:", response.text)


if __name__ == "__main__":
    asyncio.run(main())
