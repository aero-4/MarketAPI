from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings

ROOT = Path(__file__).resolve().parents[1]
MODELS: list[str] = [
    "src.payments.models",
    "src.questions.models",
    "src.reviews.models",
    "src.items.models",
    "src.wish.models",
    "src.orders.models",
    "src.models",
    "aerich.models"
]
DEFAULT_MEDIA_ALLOWED_MIMES = ["image/png", "image/jpeg", "image/jpg", "video/mp4"]
DEFAULT_MEDIA_MAX_FILE_SIZE = 50 * 1024 * 1024



class Settings(BaseSettings):
    TITLE: str = "Bazar"
    DESCRIPTION: str = "API for developers BazarMarket"

    ENV: str = "development"
    DEBUG: bool = True

    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str
    REDIS_URL: str
    DOMAIN_API: str

    ALLOWED_HOSTS: list[str] = ["*"]

    EMAIL_APP: str
    PASSWORD_APP: str
    SMTP_SERVER: str
    SMTP_PORT: int

    NOTISEND_PROJECT: str
    NOTISEND_API_KEY: str

    @field_validator("ALLOWED_HOSTS", mode="before")
    def split_hosts(cls, v):
        if isinstance(v, str):
            return [h.strip() for h in v.split(",") if h.strip()]
        return v


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

TORTOISE_ORM = {
    "connections": {
        "default": settings.DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": MODELS,
            "default_connection": "default",
        },
    },
}
