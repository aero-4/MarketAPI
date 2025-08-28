from pathlib import Path

import pytest
import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os
from tortoise import Tortoise

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

ROOT = Path(__file__).resolve().parents[1]
ENV = ROOT / ".env"
if ENV.exists():
    for line in ENV.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

CERTS = ROOT / "certs"
if CERTS.exists():
    pub = CERTS / "public.pem"
    priv = CERTS / "private.pem"
    if pub.exists():
        os.environ.setdefault("JWT_PUBLIC_KEY", pub.read_text(encoding="utf-8"))
    if priv.exists():
        os.environ.setdefault("JWT_PRIVATE_KEY", priv.read_text(encoding="utf-8"))

os.environ.setdefault("ALLOWED_HOSTS", "['*']")


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def init_db():
    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(
        Tortoise.init(
            db_url=db_url,
            modules={"models": MODELS},
        )
    )
    loop.run_until_complete(Tortoise.generate_schemas())

    yield

    loop.run_until_complete(Tortoise._drop_databases())
    loop.run_until_complete(Tortoise.close_connections())
    Tortoise.apps = {}
    loop.close()
#
#
# def random_suffix(n=8):
#     return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))
#
#
# @pytest_asyncio.fixture(scope="session", autouse=True)
# async def init_db():
#     """
#     Создаёт временную БД на сессию и инициализирует Tortoise в том же event loop,
#     который pytest-asyncio использует для тестов — это убирает ошибки с разными loops.
#     """
#     db_template = os.environ.get(
#         "TORTOISE_TEST_DB",
#         "postgres://postgres:hookklo@localhost:5432/test_{}"
#     )
#
#     # подставляем уникальное имя, чтобы каждый запуск был изолирован
#     if "{}" in db_template:
#         suffix = random_suffix()
#         db_url = db_template.format(suffix)
#         db_name = db_url.rsplit("/", 1)[-1]
#     else:
#         db_url = db_template
#         db_name = urlparse(db_url).path.lstrip("/")
#
#     parsed = urlparse(db_url)
#     pg_user = parsed.username
#     pg_password = parsed.password
#     pg_host = parsed.hostname or "localhost"
#     pg_port = parsed.port or 5432
#
#     # 1) создаём базу через обычное asyncpg-соединение (в этом же loop)
#     admin_conn = await asyncpg.connect(
#         user=pg_user, password=pg_password, host=pg_host, port=pg_port, database="postgres"
#     )
#     try:
#         try:
#             await admin_conn.execute(f'CREATE DATABASE "{db_name}"')
#         except Exception:
#             # если уже существует — игнорируем
#             pass
#     finally:
#         await admin_conn.close()
#
#     # 2) инициализация Tortoise в том же loop (важно!)
#     await Tortoise.init(
#         config={
#             "connections": {
#                 "default": {
#                     "engine": "tortoise.backends.asyncpg",
#                     "credentials": {
#                         "host": pg_host,
#                         "port": pg_port,
#                         "user": pg_user,
#                         "password": pg_password,
#                         "database": db_name,
#                         "min_size": 1,
#                         "max_size": 4,
#                     },
#                 }
#             },
#             "apps": {
#                 "models": {
#                     "models": MODELS,
#                     "default_connection": "default",
#                 }
#             },
#         }
#     )
#     await Tortoise.generate_schemas()
#
#     yield  # <- здесь запускаются тесты
#
#     # Teardown — закрываем и удаляем БД (в этом же loop)
#     await Tortoise._drop_databases()
#     await Tortoise.close_connections()
#
#     admin_conn = await asyncpg.connect(
#         user=pg_user, password=pg_password, host=pg_host, port=pg_port, database="postgres"
#     )
#     try:
#         await admin_conn.execute(
#             f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{db_name}' AND pid <> pg_backend_pid();"
#         )
#         await admin_conn.execute(f'DROP DATABASE IF EXISTS "{db_name}"')
#     finally:
#         await admin_conn.close()

