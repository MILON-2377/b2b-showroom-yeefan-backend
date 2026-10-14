import pytest

from app.core.security.authorization import has_permission
from app.core.security.permissions import Permissions
from app.modules.auth.models.user import UserRole


@pytest.mark.parametrize(
    ("role", "permission", "expected"),
    [
        # ADMIN
        (
            UserRole.ADMIN,
            Permissions.PRODUCT_MANAGE,
            True,
        ),
        (
            UserRole.ADMIN,
            Permissions.CATEGORY_MANAGE,
            True,
        ),
        (
            UserRole.ADMIN,
            Permissions.USER_CREATE,
            False,
        ),
        (
            UserRole.ADMIN,
            Permissions.USER_DEACTIVATE,
            False,
        ),
        # SUPER_ADMIN
        (
            UserRole.SUPER_ADMIN,
            Permissions.PRODUCT_MANAGE,
            True,
        ),
        (
            UserRole.SUPER_ADMIN,
            Permissions.USER_CREATE,
            True,
        ),
        (
            UserRole.SUPER_ADMIN,
            Permissions.USER_DEACTIVATE,
            True,
        ),
        # No role
        (
            None,
            Permissions.PRODUCT_MANAGE,
            False,
        ),
        (
            None,
            Permissions.USER_CREATE,
            False,
        ),
    ],
)
def test_has_permission(
    role,
    permission,
    expected,
):
    assert (
        has_permission(
            role=role,
            permission=permission,
        )
        is expected
    )
