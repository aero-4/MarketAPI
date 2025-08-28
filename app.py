import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from src import routers
from src.config import MODELS, settings
from src.exceptions import AppException
from src.handlers import app_exception_handler
from src.middlewares.ratelimit import get_redis

redis_client: Redis | None = None
FORMAT = '%(asctime)s | %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

app = FastAPI(
    title=f"{settings.TITLE} API",
    description=settings.DESCRIPTION,
    root_path=settings.API_V1_STR
)

# @app.on_event("startup")
# async def startup_event():
#     global redis_client
#     redis_client = get_redis()
#     try:
#         await redis_client.ping()
#         print("Redis connected")
#     except Exception as exc:
#         print("Warning: Redis unavailable:", exc)
#         redis_client = None
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     global redis_client
#     if redis_client:
#         await redis_client.close()
#         await redis_client.connection_pool.disconnect()
#         print("Redis closed")

for r in routers:
    app.include_router(r)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=len(settings.ALLOWED_HOSTS) > 0,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_exception_handler(AppException, app_exception_handler)

register_tortoise(
    app,
    db_url=settings.DATABASE_URL,
    modules={"models": MODELS},
    add_exception_handlers=True,
    generate_schemas=True
)
