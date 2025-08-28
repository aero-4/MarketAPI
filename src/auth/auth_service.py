import random
import uuid
from datetime import timedelta

from redis.asyncio import Redis
from starlette import status
from starlette.responses import JSONResponse

from src.auth.config import auth_settings
from src.auth.schemas import SentCodeSchema, TokensInfo
from src.config import settings
from src.models import User, RefreshToken
from src.services.codes.phone import Phone
from src.utils import encode_jwt



async def generate_auth_session_cookies(_user: User) -> TokensInfo:
    user = {
        'id': _user.id,
        'first_name': _user.first_name,
        'full_name': _user.full_name,
        'date_at': _user.date_at.strftime('%Y-%m-%d %H:%M:%S'),
        'role': _user.role
    }

    jti = str(uuid.uuid4())
    access_token = encode_jwt({'sub': str(_user.id), 'user': user, 'jti': jti, 'type': 'access'}, expire_timedelta=auth_settings.ACCESS_TOKEN_EXP)
    refresh_token = encode_jwt({'sub': str(_user.id), 'user': user, 'jti': jti, 'type': 'refresh'}, expire_timedelta=auth_settings.REFRESH_TOKEN_EXP)

    await RefreshToken.create(
        user_id=_user.id,
        jti=jti
    )
    return TokensInfo(access_token=access_token, refresh_token=refresh_token)


async def send_code(schema: SentCodeSchema, redis: Redis):
    random_num = random.randint(100000, 999999)
    await Phone().sent_code(schema.phone, random_num)

    minutes = 1
    if await redis.get(schema.phone):
        minutes += 1

    await redis.set(schema.phone,
                    random_num,
                    ex=timedelta(minutes=minutes))
