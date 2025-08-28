import datetime
from typing import List

from starlette import status
from starlette.exceptions import HTTPException

from src.exceptions import NotFound, AlreadyExist
from src.items.models import Item
from src.orders.models import Order, OrderStatus


async def get_cart_all(user) -> List[dict]:
    return await Order.filter(user_id=user.id, status=OrderStatus.IN_CART).all().values()


async def add_cart_item(schema) -> Order:
    if await Order.get_or_none(item=schema.item):
        raise AlreadyExist()

    get_seller = await Item.get_or_none(id=schema.item)
    seller = await get_seller.seller
    new_cart_item = await Order.create(
        user_id=schema.user.id,
        item_id=schema.item,
        seller_id=seller.id,
        params=schema.params,
        status=OrderStatus.IN_CART,
    )
    return new_cart_item


async def remove_cart_item(id: int) -> None:
    order = await Order.get_or_none(id=id)
    if not order:
        raise NotFound()

    await order.delete()


async def clear_cart(user):
    return await Order.filter(user=user, status=OrderStatus.IN_CART).delete()

