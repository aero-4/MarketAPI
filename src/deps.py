from cachetools.func import lru_cache
from redis.asyncio import Redis

from src.config import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_redis() -> Redis:
    return Redis.from_url(get_settings().REDIS_URL, decode_responses=True)
