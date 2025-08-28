from fastapi import Depends, HTTPException
from starlette import status

from src.auth.enums import UserRoles
from src.exceptions import NotPermissions
from src.session.depends import validate_access_token
from src.models import User


async def validate_admin_role(user: User = Depends(validate_access_token)) -> User:
    if user.role <= UserRoles.MODER:
        raise NotPermissions()
    return user
