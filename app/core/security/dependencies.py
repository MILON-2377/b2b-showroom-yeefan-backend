from typing import Annotated

from fastapi import Depends

from app.core.security.authorization import has_permission
from app.core.security.permissions import Permissions
from app.modules.auth.dependencies import require_authenticated_user
from app.modules.auth.dtos.auth_context import AuthContext
from app.modules.auth.exceptions import InsufficientPermissionsError


class RequirePermission:
    def __init__(self, permission: Permissions) -> None:
        self.permission = permission

    async def __call__(
        self,
        auth_context: Annotated[
            AuthContext,
            Depends(require_authenticated_user),
        ],
    ) -> AuthContext:

        if not has_permission(
            role=auth_context.user.role,
            permission=self.permission,
        ):
            raise InsufficientPermissionsError()

        return auth_context
