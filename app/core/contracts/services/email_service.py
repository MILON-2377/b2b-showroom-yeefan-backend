from abc import ABC, abstractmethod


class AbstractEmailService(ABC):
    @abstractmethod
    async def send_login_code(
        self,
        *,
        to_email: str,
        code: str,
    ) -> None:
        raise NotImplementedError
