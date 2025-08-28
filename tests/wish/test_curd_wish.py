import importlib
import json
import random
from types import SimpleNamespace

import pytest
from src.exceptions import NotFound
from src.wish.schemas import *


@pytest.fixture(autouse=True)
async def clear_db():
    from src.items.models import Item
    from src.wish.models import Wish

    yield
    await Wish.all().delete()
    await Item.all().delete()


@pytest.mark.asyncio
async def test_get_wish_all():
    # reload service to ensure fresh state
    wish_service = importlib.import_module("src.wish.wish_service")
    importlib.reload(wish_service)

    from src.models import User, UserRoles
    from src.items.models import Item
    from src.wish.models import Wish

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    item1 = await Item.create(title="I1", seller=seller, description="d", price=1, discount_price=1, params=json.dumps({}), cat="c", sub_cat="s", count_all=1, article_id=1)
    item2 = await Item.create(title="I2", seller=seller, description="d2", price=2, discount_price=1, params=json.dumps({}), cat="c", sub_cat="s", count_all=1, article_id=2)

    w1 = await Wish.create(user=user, item=item1, cat="foo")
    w2 = await Wish.create(user=user, item=item2, cat="bar")

    res = await wish_service.get_wish_all(user, "foo")
    res2 = await wish_service.get_wish_all(user, "bar")

    assert isinstance(res, list)

    returned_ids = {w.id for w in res}
    returned_ids2 = {w.id for w in res2}

    assert w1.id in returned_ids and w2.id in returned_ids2


@pytest.mark.asyncio
async def test_get_wish_item_not_found_raises():
    wish_service = importlib.import_module("src.wish.wish_service")
    importlib.reload(wish_service)

    from src.models import User, UserRoles

    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    # use non-existent item id
    schema = SimpleNamespace(item=9999999, category="doesnt_matter")
    # Expect NotFound because Item.get_or_none(id=schema.item) will be falsy
    with pytest.raises(NotFound):
        await wish_service.get_wish(schema, user)


@pytest.mark.asyncio
async def test_get_wish_success_and_delete():
    wish_service = importlib.import_module("src.wish.wish_service")
    importlib.reload(wish_service)
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)

    from src.models import User, UserRoles
    from src.items.models import Item
    from src.wish.models import Wish

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    item = await items_service.create_item(
        title="Q item 3",
        seller=seller,
        description="desc3",
        price=30,
        discount_price=15,
        params=json.dumps({"brand": "Y"}),
        cat="food",
        sub_cat="food",
        count_all=1,
    )

    # create wish with category "for my cat"
    schema = WishSchema(user=user.id, item=item.id, cat="for my cat")

    wish = await wish_service.add_wish(schema, user)
    assert isinstance(wish, Wish)

    schema2 = WishSchema(user=user.id, item=item.id)
    wish2 = await wish_service.add_wish(schema2, user)
    assert isinstance(wish2, Wish)

    # delete and ensure removed
    deleted = await wish_service.delete_wish(schema, user)
    assert deleted.id == wish.id

    # fetch should return None from DB
    should_be_none = await Wish.get_or_none(id=wish.id)
    assert should_be_none is None
