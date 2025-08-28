import asyncio
import importlib
import json
import random

import pytest
from pydantic import BaseModel

from src.items.schemas import LastItemsSchema
from src.models import User
from src.search.schemas import SearchResultSchema


@pytest.fixture(autouse=True)
async def clear_db():
    from src.items.models import Item
    from src.models import Media, Attachment

    yield
    await Attachment.all().delete()
    await Media.all().delete()
    await Item.all().delete()


@pytest.mark.asyncio
async def test_last_items_success():
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)
    seller = await User.create(phone=random.randint(1, 100000))
    await asyncio.gather(*[
        items_service.create_item(
            title="Smartphone Iphone 15 PRO MAX",
            seller=seller,
            description="rand desc",
            price=60000,
            discount_price=39800 + _,
            params=json.dumps({"brand": "Iphone"}),
            cat="electronics",
            sub_cat="smartphone",
            count_all=12,
        ) for _ in range(25)
    ])

    offset = 0
    limit = 45
    schema = LastItemsSchema(offset=offset, limit=limit)
    last_items = await items_service.last_items(schema)

    assert isinstance(last_items, SearchResultSchema)
    assert last_items.limit != limit  # MAX LIMIT 40


@pytest.mark.asyncio
async def test_last_items_null():
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)

    offset = 0
    limit = 40
    schema = LastItemsSchema(offset=offset, limit=limit)
    last_items = await items_service.last_items(schema)

    assert isinstance(last_items, SearchResultSchema)
    assert last_items.data == []


@pytest.mark.asyncio
async def test_last_items_offset_limit():
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)

    seller = await User.create(phone=random.randint(1, 100000))
    await asyncio.gather(*[
        items_service.create_item(
            title="Smartphone Iphone 15 PRO MAX",
            seller=seller,
            description="rand desc",
            price=60000,
            discount_price=39800 + _,
            params=json.dumps({"brand": "Iphone"}),
            cat="electronics",
            sub_cat="smartphone",
            count_all=12,
        ) for _ in range(25)
    ])

    offset = 1
    limit = 2
    schema = LastItemsSchema(offset=offset, limit=limit)
    last_items = await items_service.last_items(schema)

    assert isinstance(last_items, SearchResultSchema)
    # assert len(last_items.data) == 2  # потому что у нас всегда +1 чтобы делать свойство has_more
    assert len(last_items.data) == 3


@pytest.mark.asyncio
async def test_get_item():
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)

    seller = await User.create(phone=random.randint(1, 100000))
    await asyncio.gather(*[
        items_service.create_item(
            title="Smartphone Iphone 15 PRO MAX",
            seller=seller,
            description="rand desc",
            price=60000,
            discount_price=39800 + _,
            params=json.dumps({"brand": "Iphone"}),
            cat="electronics",
            sub_cat="smartphone",
            count_all=12,
        ) for _ in range(35)
    ])

    item = await items_service.get_item(7)


    assert item['item']['title'] == "Smartphone Iphone 15 PRO MAX"
    assert len(item["similar_items"]) == 25
