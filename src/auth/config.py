from datetime import timedelta
from typing import Optional

from cachetools.func import lru_cache
from pydantic import validator, field_validator
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


class AuthConfig(BaseSettings):
    JWT_PUBLIC_KEY: Optional[str] = None
    JWT_PRIVATE_KEY: Optional[str] = None

    JWT_ALG: str = "RS256"
    ACCESS_TOKEN_EXP: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXP: timedelta = timedelta(days=30)

    @field_validator("JWT_PUBLIC_KEY", mode='after')
    def load_public(cls, v):
        if v:
            return v
        return (BASE_DIR / "certs" / "public.pem").read_text()

    @field_validator("JWT_PRIVATE_KEY", mode='after')
    def load_private(cls, v):
        if v:
            return v
        return (BASE_DIR / "certs" / "private.pem").read_text()


@lru_cache(maxsize=1024)
def get_auth_settings():
    return AuthConfig()


auth_settings = get_auth_settings()
