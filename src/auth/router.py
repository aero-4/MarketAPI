from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from src.auth.auth_service import generate_auth_session_cookies, send_code
from src.auth.config import auth_settings
from src.auth.depends import validate_login_user
from src.auth.schemas import SentCodeSchema, TokensInfo
from src.config import settings
from src.middlewares.ratelimit import get_redis
from src.models import User
from src.utils import response

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
IS_PROD = settings.ENV != "developemnt"


@auth_router.post("/sent-code")
async def sent_code(schema: SentCodeSchema, redis=Depends(get_redis)):
    await send_code(schema, redis)
    return response(status.HTTP_200_OK,
                    message="Code sent")


@auth_router.post("/login", response_model=TokensInfo)
async def login_handler(user: User = Depends(validate_login_user)):
    tokens_data = await generate_auth_session_cookies(user)
    response = JSONResponse(status_code=status.HTTP_200_OK, content=tokens_data)
    response.set_cookie("access_token", tokens_data.access_token, samesite="lax", secure=IS_PROD, expires=auth_settings.ACCESS_TOKEN_EXP, path="/")
    response.set_cookie("refresh_token", tokens_data.refresh_token, samesite="lax", secure=IS_PROD, expires=auth_settings.REFRESH_TOKEN_EXP, path="/")
    return response
