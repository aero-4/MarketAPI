from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse, Response

from src.auth.schemas import TokensInfo
from src.config import settings
from src.models import User
from src.session.depends import validate_refresh_token
from src.session.session_service import logout_user, refresh_access_token

session_router = APIRouter(prefix="/session", tags=["Session"])
IS_PROD = settings.ENV != "developemnt"


@session_router.post("/refresh", response_model=TokensInfo)
async def refresh_token(user: tuple[User, str] = Depends(validate_refresh_token)):
    tokens: TokensInfo = await refresh_access_token(user[0])
    response = JSONResponse(status_code=200, content={'access_token': tokens.access_token})
    response.set_cookie("access_token", tokens.access_token, samesite="lax", secure=IS_PROD, max_age=15 * 60 * 60)
    return response


@session_router.post("/logout")
async def logout_handler(response: Response, user=Depends(validate_refresh_token)):
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/")
    return await logout_user(user)
