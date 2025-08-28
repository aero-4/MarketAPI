from fastapi import HTTPException, Depends
from starlette import status

from src.auth.enums import UserRoles
from src.models import User
from src.session.depends import validate_access_token


async def validate_seller_role(user: User = Depends(validate_access_token)):
    if user.role <= UserRoles.USER:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No rights for this")

    return user