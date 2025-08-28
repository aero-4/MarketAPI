import importlib
import pytest
from fastapi import exceptions, HTTPException

from src.auth.schemas import TokensInfo
from src.exceptions import NotFound
from src.models import User
from src.session.depends import validate_access_token, validate_refresh_token
from src.session.session_service import refresh_access_token, logout_user


@pytest.fixture(autouse=True)
async def clear_db():
    from src.models import User, RefreshToken
    yield
    await User.all().delete()
    await RefreshToken.all().delete()


@pytest.mark.asyncio
async def test_auth_login_user_tokens():
    auth_service = importlib.import_module("src.auth.auth_service")
    importlib.reload(auth_service)

    phone = 12345
    user = await User.create(phone=phone)
    tokens: TokensInfo = await auth_service.generate_auth_session_cookies(user)
    assert isinstance(tokens, TokensInfo)
    assert isinstance(tokens.refresh_token, str)
    assert isinstance(tokens.access_token, str)

    check_access = await validate_access_token(tokens.access_token)
    assert isinstance(check_access, User)
    assert check_access.phone == phone


@pytest.mark.asyncio
async def test_auth_login_logout_and_revoke_refresh_token():
    auth_service = importlib.import_module("src.auth.auth_service")
    importlib.reload(auth_service)

    phone = 777
    user = await User.create(phone=phone)
    tokens: TokensInfo = await auth_service.generate_auth_session_cookies(user)

    jti = await validate_refresh_token(tokens.refresh_token)
    new_access: TokensInfo = await refresh_access_token(user)
    tokens.access_token = new_access.access_token

    assert isinstance(jti, str)

    await logout_user(jti)

    with pytest.raises(NotFound) as exp:
        await logout_user(jti)


@pytest.mark.asyncio
async def test_check_authorization_access_token():
    auth_service = importlib.import_module("src.auth.auth_service")
    importlib.reload(auth_service)

    phone = 777
    user = await User.create(phone=phone)
    tokens: TokensInfo = await auth_service.generate_auth_session_cookies(user)
    user = await validate_access_token(tokens.access_token)

    assert user.phone == phone

    with pytest.raises(exceptions.HTTPException) as exp1:
        # random string
        await validate_access_token("128738192738927ads897vad9a87daj89")
        assert exp1.value.status_code == 402

    with pytest.raises(exceptions.HTTPException) as exp2:
        # del last symbol
        await validate_access_token(tokens.access_token[:-1])
        assert exp2.value.status_code == 403

    with pytest.raises(exceptions.HTTPException) as exp3:
        # check refresh
        await validate_access_token(tokens.refresh_token)
        assert exp3.value.status_code == 400


@pytest.mark.asyncio
async def test_refresh_token():
    auth_service = importlib.import_module("src.auth.auth_service")
    importlib.reload(auth_service)

    phone = 777
    user = await User.create(phone=phone)
    tokens: TokensInfo = await auth_service.generate_auth_session_cookies(user)


    jti = await validate_refresh_token(tokens.refresh_token)
    new_refresh = await refresh_access_token(user)

    assert isinstance(new_refresh, TokensInfo)

    await logout_user(jti)

    # revoked token NO REFRESH
    with pytest.raises(HTTPException):
        jti = await validate_refresh_token(tokens.refresh_token)
