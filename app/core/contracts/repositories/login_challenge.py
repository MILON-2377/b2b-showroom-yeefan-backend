from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.modules.auth.models.login_challenge import LoginChallenge


class AbstractLoginChallengeRepository(ABC):
    @abstractmethod
    async def get_by_id_for_update(
        self,
        *,
        challenge_id: UUID,
    ) -> LoginChallenge | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        *,
        challenge_id: UUID,
    ) -> LoginChallenge | None:
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        challenge: LoginChallenge,
    ) -> LoginChallenge: ...

    @abstractmethod
    async def get_latest_active_by_user_id(
        self,
        *,
        user_id: UUID,
        now: datetime,
    ) -> LoginChallenge | None: ...

    @abstractmethod
    async def invalidate_active_by_user_id(
        self,
        *,
        user_id: UUID,
        now: datetime,
    ) -> None: ...

    @abstractmethod
    async def update(
        self,
        challenge: LoginChallenge,
    ) -> LoginChallenge: ...
