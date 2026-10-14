from app.core.security.permissions import Permissions
from app.core.security.roles import ROLE_PERMISSIONS
from app.modules.auth.models.user import UserRole


def has_permission(
    *,
    role: UserRole | None,
    permission: Permissions,
) -> bool:
    if role is None:
        return False

    permissions = ROLE_PERMISSIONS.get(role)

    if permissions is None:
        return False

    return permission in permissions
