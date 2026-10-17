from uuid import UUID

from app.core.errors.base import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)


class InvalidCredentialsError(ValidationError):
    """Raised when authentication credentials are invalid."""

    def __init__(self) -> None:
        super().__init__(
            "Invalid email or password",
            code="INVALID_CREDENTIALS",
        )


class UserNotFoundError(NotFoundError):
    """Raised when an authenticated user cannot be found."""

    def __init__(self, user_id: UUID) -> None:
        super().__init__(
            "User not found",
            code="USER_NOT_FOUND",
        )
        self.user_id = user_id


class UserEmailAlreadyExistsError(ConflictError):
    """Raised when a user with the given email already exists."""

    def __init__(self, email: str) -> None:
        super().__init__(
            "A user with this email already exists",
            code="USER_EMAIL_ALREADY_EXISTS",
        )
        self.email = email


class UserInactiveError(UnauthorizedError):
    """Raised when an inactive user attempts to authenticate."""

    def __init__(self) -> None:
        super().__init__(
            "User account is inactive",
            code="USER_INACTIVE",
        )


class InvalidAccessTokenError(UnauthorizedError):
    """Raised when an access token is invalid or cannot be verified."""

    def __init__(self) -> None:
        super().__init__(
            "Invalid access token",
            code="INVALID_ACCESS_TOKEN",
        )


class AccessTokenExpiredError(UnauthorizedError):
    """Raised when an access token has expired."""

    def __init__(self) -> None:
        super().__init__(
            "Access token has expired",
            code="ACCESS_TOKEN_EXPIRED",
        )


class InvalidRefreshTokenError(UnauthorizedError):
    def __init__(self) -> None:
        super().__init__(
            "Invalid refresh token",
            code="INVALID_REFRESH_TOKEN",
        )


class RefreshTokenExpiredError(UnauthorizedError):
    def __init__(self) -> None:
        super().__init__(
            "Refresh token has expired",
            code="REFRESH_TOKEN_EXPIRED",
        )


class RefreshTokenReuseDetectedError(ConflictError):
    """
    Raised when a previously rotated refresh token is used again.

    This indicates possible refresh-token theft or replay.
    """

    def __init__(self, family_id: UUID) -> None:
        super().__init__(
            "Refresh token reuse detected",
            code="REFRESH_TOKEN_REUSE_DETECTED",
        )
        self.family_id = family_id


class SessionNotFoundError(NotFoundError):
    """Raised when a session cannot be found."""

    def __init__(self, session_id: UUID) -> None:
        super().__init__(
            "Session not found",
            code="SESSION_NOT_FOUND",
        )
        self.session_id = session_id


class SessionRevokedError(UnauthorizedError):
    def __init__(self, session_id: UUID):
        super().__init__(
            f"Session {session_id} has been revoked.",
            code="SESSION_REVOKED",
        )


class SessionExpiredError(UnauthorizedError):
    def __init__(self, session_id: UUID):
        super().__init__(
            f"Session {session_id} has expired.",
            code="SESSION_EXPIRED",
        )


class UnauthorizedSessionAccessError(ValidationError):
    """Raised when a user attempts to access another user's session."""

    def __init__(self, session_id: UUID) -> None:
        super().__init__(
            "You do not have access to this session",
            code="UNAUTHORIZED_SESSION_ACCESS",
        )
        self.session_id = session_id


class InsufficientPermissionsError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            "You do not have permission to perform this action",
            code="INSUFFICIENT_PERMISSIONS",
        )


class UserProfileNotFoundError(NotFoundError):
    def __init__(self, user_id: UUID) -> None:
        super().__init__(
            "User profile not found",
            code="USER_PROFILE_NOT_FOUND",
            details={"user_id": str(user_id)},
        )


class CannotDeactivateOwnAccountError(ForbiddenError):
    def __init__(self) -> None:
        super().__init__(
            "You cannot deactivate your own account.",
            code="CANNOT_DEACTIVATE_OWN_ACCOUNT",
        )


class InvalidLoginChallengeError(UnauthorizedError):
    """Raised when a login verification challenge is invalid."""

    def __init__(self) -> None:
        super().__init__(
            "Invalid or already-used login verification code",
            code="INVALID_LOGIN_CHALLENGE",
        )


class LoginChallengeExpiredError(UnauthorizedError):
    """Raised when a login verification challenge has expired."""

    def __init__(self) -> None:
        super().__init__(
            "Login verification code has expired. Please request a new code.",
            code="LOGIN_CHALLENGE_EXPIRED",
        )


class LoginChallengeAttemptsExceededError(ForbiddenError):
    """Raised when the maximum number of login verification attempts is exceeded."""

    def __init__(self) -> None:
        super().__init__(
            "Too many incorrect verification attempts. Please request a new code.",
            code="LOGIN_CHALLENGE_ATTEMPTS_EXCEEDED",
        )
