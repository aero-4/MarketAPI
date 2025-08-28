# test_items_real_db.py
import io
import json
import datetime
import random
import pytest
from httpx import AsyncClient, WSGITransport, ASGITransport
from tortoise import Tortoise

from app import app
from src.items.depends import validate_seller_role
from src.items.params_schemas import SmartphoneParams
from src.models import User


@pytest.fixture(scope="session", autouse=True)
async def init_test_db():
    # Инициализация тестовой БД
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["src.models"]},
    )
    await Tortoise.generate_schemas()

    # Создаём тестового пользователя
    test_user = await User.create(
        id=3,
        username="test_seller",
        email="test_seller@example.com",
        role=0,
    )

    yield {"user": test_user}

    await Tortoise._drop_databases()
    await Tortoise.close_connections()


async def override_validate_seller_role():
    return await User.get(id=3)


@pytest.mark.asyncio
async def test_create_item_with_real_db(init_test_db):
    app.dependency_overrides[validate_seller_role] = override_validate_seller_role

    files = [
        ("media_files", ("img1.jpg", io.BytesIO(b"first file bytes"), "image/jpeg")),
    ]
    data = {
        "title": "My item",
        "description": "Описание товара",
        "count_all": str(10),
        "price": str(999),
        "discount": str(5.5),
        "cat": "electronics",
        "sub_cat": "smartphone",
        "params": json.dumps(
            SmartphoneParams(
                brand=str(random.randint(1, 100)),
                model=str(random.randint(1, 100)),
                price=str(random.randint(1, 100)),
                release_date=str(datetime.date.today()),
                screen_size=6.8,
                battery_capacity=3800,
                ram=16,
                storage=32,
                camera_megapixels=13.0,
                os="Apple",
                connectivity=["5G", "Wifi"],
            ).model_dump()
        ),
    }

    async with AsyncClient(transport=ASGITransport(app), base_url="http://test/api") as client:
        response = await client.post("/items/create", files=files, data=data)

    assert response.status_code == 200
    print(response.json())
