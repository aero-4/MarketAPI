import asyncio

from fastapi import HTTPException
from redis.asyncio.client import Redis
from starlette import status
from starlette.requests import Request
from functools import wraps, lru_cache

from src.cache.redis_client import incr_with_expire
from src.config import get_settings
from src.deps import get_redis


def get_ip_client(request: Request) -> str:
    xff = request.headers.get('X-Forwarded-For')
    ip = xff.split(',')[0].strip() if xff else request.client.host
    return "ip:" + ip


def rate_limit(limit: int, window: int, key_func=None, prefix: str = "rl", error_msg: str = "Too many requests"):
    def decorator(func):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("rate_limit - decorator only supports async function")

        @wraps(func)
        async def wrapper(*args, **kwargs):
            if key_func:
                try:
                    rate_key_suffix = key_func(*args, **kwargs)
                except Exception as e:
                    rate_key_suffix = f"{func.__module__}.{func.__name__}"

            else:
                rate_key_suffix = f"{func.__module__}.{func.__name__}"

            key = f"{prefix}:{rate_key_suffix}:{window}"

            r = get_redis()

            try:
                cnt = await incr_with_expire(r, key, window)

            except Exception as e:
                print("Rate limiter redis error (allowing):", e)
                return await func(*args, **kwargs)

            if cnt > limit:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=error_msg)

            return await func(*args, **kwargs)

        return wrapper

    return decorator
