import uuid

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.auth.config import auth_settings
from src.auth.schemas import UserSchema, TokensInfo
from src.exceptions import NotFound
from src.models import User, RefreshToken
from src.utils import encode_jwt


async def refresh_access_token(user: User) -> TokensInfo:
    _user = UserSchema(id=user.id, first_name=user.first_name, full_name=user.full_name, date_at=str(user.date_at), email=user.email, role=user.role)
    jti = str(uuid.uuid4())
    access_token = encode_jwt({'sub': str(user.id), 'user': _user.dict(), 'jti': jti, 'type': 'access'}, expire_timedelta=auth_settings.REFRESH_TOKEN_EXP)
    await RefreshToken.create(
        user_id=user.id,
        jti=jti
    )
    return TokensInfo(access_token=access_token)


async def logout_user(jti: str) -> None:
    refresh = await RefreshToken.get_or_none(jti=jti)
    if not refresh or refresh.revoked:
        raise NotFound()

    refresh.revoked = True
    await refresh.save()
