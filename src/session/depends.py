from starlette import status
from fastapi import HTTPException, Cookie, Depends

from src.auth.schemas import UserSchema
from src.models import User, RefreshToken
from src.utils import decode_jwt


async def is_token_revoked(jti: str):
    token = await RefreshToken.get_or_none(jti=jti)
    if token.revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")


async def validate_refresh_token(refresh_token: str | None = Cookie(None, alias="refresh_token")) -> str:
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorization")

    payload = decode_jwt(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong token type")

    user = UserSchema.model_validate(payload.get("user"))
    if not (user := await User.get_or_none(id=user.id)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    await is_token_revoked(payload.get("jti"))
    return payload["jti"]


async def validate_access_token(access_token: str | None = Cookie(None, alias="access_token")) -> User:
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorization")

    payload = decode_jwt(access_token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong token type")

    user = UserSchema.model_validate(payload.get("user"))
    if not (user := await User.get_or_none(id=user.id)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user
