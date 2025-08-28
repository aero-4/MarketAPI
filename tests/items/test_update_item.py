import importlib
import json
import random

import pytest
from fastapi import HTTPException

from src.auth.enums import UserRoles
from src.exceptions import NotFound
from src.items.models import Item
from src.items.schemas import UpdateItemSchema
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
async def test_update_item_found_success():
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
    assert item.id == 1
    schema = UpdateItemSchema(id=item.id, title="IPHONE 7", description="NEW PHONE IPHONE", price=18700)
    await item_service.update_item(schema, seller.id)

    item2 = await Item.get_or_none(id=schema.id)

    assert item2.title == "IPHONE 7"
    assert item2.description == "NEW PHONE IPHONE"
    assert item2.price == 18700
