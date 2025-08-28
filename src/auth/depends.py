import datetime

from fastapi import Body, Depends
from starlette import status
from starlette.exceptions import HTTPException

from src.auth.schemas import LoginSchema
from src.middlewares.ratelimit import get_redis
from src.models import User


async def validate_login_user(login_schema: LoginSchema = Body(...), redis=Depends(get_redis)) -> User:
    user = await User.get_or_none(phone=login_schema.phone)
    code = await redis.get(login_schema.phone)

    if not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Code expired")

    code = int(code)
    if code != login_schema.code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not valid code")

    if not user:
        user = await User.create(
            date_at=datetime.datetime.now(),
            phone=login_schema.phone,
        )
    return user
