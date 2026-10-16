import logging
import secrets
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.core.config import settings
from app.core.contracts.services.auth import AbstractAuthService
from app.core.contracts.services.auth_session import AbstractSessionService
from app.core.contracts.services.token import AbstractTokenService
from app.core.contracts.unit_of_work import AbstractUnitOfWork
from app.core.security.password_manager import PasswordManager
from app.modules.auth.dtos.auth import AuthTokensDTO
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.auth.exceptions import (
    InvalidAccessTokenError,
    InvalidCredentialsError,
    InvalidRefreshTokenError,
    RefreshTokenExpiredError,
    RefreshTokenReuseDetectedError,
    SessionExpiredError,
    SessionRevokedError,
    UserEmailAlreadyExistsError,
    UserInactiveError,
    UserNotFoundError,
)
from app.modules.auth.models.refresh_token import RefreshToken
from app.modules.auth.models.session import Session
from app.modules.auth.models.user import User

logger = logging.getLogger(__name__)


# Auth Service
class AuthService(AbstractAuthService):
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        password_manager: PasswordManager,
        token_service: AbstractTokenService,
        session_service: AbstractSessionService,
    ):

        self.uow = uow
        self.password_manager = password_manager
        self.token_service = token_service
        self.session_service = session_service

    async def register(
        self,
        *,
        email: str,
        password: str,
    ) -> User:
        existing_user = await self.uow.users.get_by_email(email)

        if existing_user is not None:
            raise UserEmailAlreadyExistsError(email)

        password_hash = self.password_manager.hash_password(password)

        user = User(
            email=email,
            password_hash=password_hash,
            role=None,
            is_active=True,
        )

        user = self.uow.users.create(user)

        await self.uow.flush()

        await self.uow.commit()

        return user

    async def login(
        self,
        email: str,
        password: str,
        device_name: str | None = None,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> AuthTokensDTO:

        user = await self.uow.users.get_by_email(email=email)

        if user is None:
            logger.warning("Login failed: account not found")
            raise InvalidCredentialsError()

        if not user.is_active:
            logger.warning("Login rejected: inactive account user_id=%s", user.id)
            raise InvalidCredentialsError()

        if not self.password_manager.verify_password(
            password,
            user.password_hash,
        ):
            logger.warning(
                "Login failed: invalid credentials user_id=%s",
                user.id,
            )
            raise InvalidCredentialsError()

        now = datetime.now(timezone.utc)

        active_sessions = await self.uow.auth_sessions.get_active_by_user_id(
            user_id=user.id
        )

        max_sessions = settings.max_sessions_per_user

        if len(active_sessions) >= max_sessions:
            session_to_revoke = active_sessions[
                : len(active_sessions) - max_sessions + 1
            ]

            for session in session_to_revoke:
                await self._revoke_session_and_tokens(session=session)

        session = Session(
            user_id=user.id,
            device_name=device_name,
            user_agent=user_agent,
            ip_address=ip_address,
            last_active_at=now,
            expires_at=self.token_service.refresh_token_expires_at(now),
        )

        await self.uow.auth_sessions.create(session)

        family_id = uuid4()

        raw_refresh_token = self.token_service.generate_refresh_token()

        refresh_token = RefreshToken(
            session_id=session.id,
            jti=secrets.token_urlsafe(32),
            family_id=family_id,
            token_hash=self.token_service.hash_refresh_token(raw_refresh_token),
            expires_at=self.token_service.refresh_token_expires_at(now),
        )

        self.uow.refresh_tokens.create(refresh_token)
        await self.uow.flush()

        access_token = self.token_service.create_access_token(
            subject=str(user.id), session_id=session.id
        )

        await self.uow.commit()

        return AuthTokensDTO(
            access_token=access_token.token,
            refresh_token=raw_refresh_token,
            token_type="bearer",
            expires_at=access_token.expires_at,
            session_id=session.id,
        )

    async def refresh(
        self,
        *,
        refresh_token: str,
    ) -> AuthTokensDTO:
        token_hash = self.token_service.hash_refresh_token(refresh_token)

        stored_token = await self.uow.refresh_tokens.get_by_token_hash(token_hash)

        if stored_token is None:
            raise InvalidRefreshTokenError()

        if stored_token.revoked_at is not None:
            await self.uow.refresh_tokens.revoke_family(stored_token.family_id)
            await self.uow.commit()

            logger.warning(
                "Refresh-token reuse detected session_id=%s",
                stored_token.session_id,
            )
            raise RefreshTokenReuseDetectedError(stored_token.family_id)

        now = datetime.now(timezone.utc)

        if stored_token.expires_at <= now:
            raise RefreshTokenExpiredError()

        session = await self.uow.auth_sessions.get_by_id(stored_token.session_id)

        if session is None:
            raise InvalidRefreshTokenError()

        if session.revoked_at is not None:
            raise SessionRevokedError(session.id)

        if session.expires_at <= now:
            raise SessionExpiredError(session.id)

        user = await self.uow.users.get_by_id(session.user_id)

        if user is None or not user.is_active:
            raise InvalidAccessTokenError()

        new_raw_refresh_token = self.token_service.generate_refresh_token()

        replacement_token = RefreshToken(
            session_id=session.id,
            jti=secrets.token_urlsafe(32),
            family_id=stored_token.family_id,
            token_hash=self.token_service.hash_refresh_token(new_raw_refresh_token),
            expires_at=self.token_service.refresh_token_expires_at(now),
        )

        await self.uow.refresh_tokens.rotate(
            current_token=stored_token,
            replacement_token=replacement_token,
        )

        session.last_active_at = now

        await self.uow.auth_sessions.update_activity(session)

        access_token = self.token_service.create_access_token(
            subject=str(user.id), session_id=session.id
        )

        await self.uow.commit()

        return AuthTokensDTO(
            access_token=access_token.token,
            refresh_token=new_raw_refresh_token,
            token_type="bearer",
            expires_at=access_token.expires_at,
            session_id=session.id,
        )

    async def logout(
        self,
        *,
        refresh_token: str,
    ) -> None:

        logger.debug("Logout requested")

        token_hash = self.token_service.hash_refresh_token(
            refresh_token,
        )

        token = await self.uow.refresh_tokens.get_by_token_hash(
            token_hash,
        )

        if token is None:
            logger.info("Logout skipped: refresh-token record not found")
            return

        if token.revoked_at is not None:
            logger.info("Logout skipped: token already revoked session_id=%s")
            return

        session = await self.uow.auth_sessions.get_by_id(token.session_id)

        if session is not None:
            await self._revoke_session_and_tokens(session=session)

        else:
            await self.uow.refresh_tokens.revoke(token)

        await self.uow.commit()

        logger.info(
            "Logout successful session_id=%s",
            token.session_id,
        )

    async def get_current_user(
        self,
        *,
        access_token: str,
    ) -> AuthContext:
        payload = self.token_service.decode_access_token(
            access_token,
        )

        if payload is None:
            raise InvalidAccessTokenError()

        subject = payload.get("sub")
        session_id_value = payload.get("sid")

        if not subject or not session_id_value:
            raise InvalidAccessTokenError()

        try:
            user_id = UUID(subject)
            session_id = UUID(session_id_value)
        except (ValueError, TypeError):
            raise InvalidAccessTokenError()

        session = await self.uow.auth_sessions.get_active_by_id(session_id)

        if session is None:
            raise InvalidAccessTokenError()

        if session.user_id != user_id:
            raise InvalidAccessTokenError()

        user = await self.uow.users.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(user_id)

        if not user.is_active:
            raise UserInactiveError()

        return AuthContext(user=user, session_id=session_id)

    async def _revoke_session_and_tokens(
        self,
        session: Session,
    ) -> None:
        refresh_tokens = await self.uow.refresh_tokens.get_active_by_session_id(
            session_id=session.id,
        )

        for refresh_token in refresh_tokens:
            await self.uow.refresh_tokens.revoke(refresh_token)

        await self.uow.auth_sessions.revoke(session)
