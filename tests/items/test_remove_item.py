import importlib
import json
import random

import pytest
from fastapi import HTTPException

from src.auth.enums import UserRoles
from src.exceptions import NotFound
from src.items.models import Item
from src.models import User


@pytest.fixture(autouse=True)
async def clear_db():
    from src.items.models import Item
    from src.models import Media, Attachment

    yield
    await Attachment.all().delete()
    await Media.all().delete()
    await Item.all().delete()


@pytest.mark.asyncio
async def test_remove_item_found_success():
    item_service = importlib.import_module("src.items.items_service")
    importlib.reload(item_service)
    seller = await User.create(phone=random.randint(1, 100000))

    item = await item_service.create_item(
        title="Smartphone Iphone 13 PRO MAX",
        seller=seller,
        description="rand desc",
        price=40000,
        discount_price=39800,
        params=json.dumps({"brand": "Iphone"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=12,
    )
    await item_service.remove_item(item.id)
    item2 = await Item.get_or_none(id=item.id)

    assert item2 is None


@pytest.mark.asyncio
async def test_remove_item_not_found():
    item_service = importlib.import_module("src.items.items_service")
    importlib.reload(item_service)
    item_id = 1
    seller = await User.create(phone=123)

    with pytest.raises(NotFound) as excInfo:
        await item_service.remove_item(item_id, seller.id)
