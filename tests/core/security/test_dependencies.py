import pytest

from app.core.security.dependencies import RequirePermission
from app.core.security.permissions import Permissions
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.auth.exceptions import InsufficientPermissionsError
from app.modules.auth.models.user import User, UserRole


def make_auth_context(role: UserRole | None) -> AuthContext:
    user = User(
        email="test@example.com",
        password_hash="hashed",
        role=role,
        is_active=True,
    )

    return AuthContext(
        user=user,
        session_id=None,
    )


@pytest.mark.asyncio
async def test_admin_can_manage_products():
    dependency = RequirePermission(
        Permissions.PRODUCT_MANAGE,
    )

    context = make_auth_context(UserRole.ADMIN)

    result = await dependency(context)

    assert result is context


@pytest.mark.asyncio
async def test_admin_cannot_create_users():
    dependency = RequirePermission(
        Permissions.USER_CREATE,
    )

    context = make_auth_context(UserRole.ADMIN)

    with pytest.raises(InsufficientPermissionsError):
        await dependency(context)


@pytest.mark.asyncio
async def test_super_admin_can_create_users():
    dependency = RequirePermission(
        Permissions.USER_CREATE,
    )

    context = make_auth_context(UserRole.SUPER_ADMIN)

    result = await dependency(context)

    assert result is context


@pytest.mark.asyncio
async def test_user_without_role_has_no_permissions():
    dependency = RequirePermission(
        Permissions.PRODUCT_MANAGE,
    )

    context = make_auth_context(None)

    with pytest.raises(InsufficientPermissionsError):
        await dependency(context)
