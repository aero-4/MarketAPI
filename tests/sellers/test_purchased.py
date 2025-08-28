import importlib
import json
from types import SimpleNamespace
import pytest

from src.auth.enums import UserRoles
from src.items.models import Item
from src.models import User
from src.orders.models import Order, OrderStatus
from src.utils import response

service = importlib.import_module("src.sellers.seller_service")
importlib.reload(service)


@pytest.mark.asyncio
async def test_change_status_purchased_success():
    phone = 78789787878
    user = await User.create(phone=phone)
    seller = await User.create(phone=123142141224, role=UserRoles.SELLER)
    item1 = await Item.create(title="I1", seller=seller, description="d", price=1, discount_price=1, params=json.dumps({}), cat="c", sub_cat="s", count_all=1, article_id=2)
    order = await Order.create(item=item1, user=user, seller=seller, status=OrderStatus.WAITING)
    print(order)

    schema = SimpleNamespace(item_id=item1.id, status=OrderStatus.IN_TRANSIT)
    new_status = await service.edit_status(schema, seller)
    assert new_status.status == schema.status

    schema = SimpleNamespace(item_id=item1.id, status=OrderStatus.READY)
    new_status = await service.edit_status(schema, seller)
    assert new_status.status == schema.status


@pytest.mark.asyncio
async def test_change_status_purchased():
    phone = 78789787878
    user = await User.create(phone=phone)
    seller = await User.create(phone=123142141224, role=UserRoles.SELLER)
    item1 = await Item.create(title="I1", seller_id=seller.id, description="d", price=1, discount_price=1, params=json.dumps({}), cat="c", sub_cat="s", count_all=1, article_id=4)
    order = await Order.create(item=item1, user=user, seller=seller, status=OrderStatus.WAITING)
    print(order)

    schema = SimpleNamespace(item_id=item1.id, status=OrderStatus.IN_TRANSIT)
    purchased_orders = await service.get_purchased_orders(seller)
    assert isinstance(purchased_orders, list)
