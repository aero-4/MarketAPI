from fastapi import HTTPException
from starlette import status
from tortoise.transactions import in_transaction

from src.models import User
from src.orders.models import Order, OrderStatus


async def get_summa_orders_cart(orders) -> int:
    summa = 0
    for o in orders:
        item = await o.item
        summa += item.price
    return summa


async def update_status_and_address(orders, delivery_address) -> None:
    for o in orders:
        o.status = OrderStatus.WAITING
        o.delivery_address = delivery_address
        await o.save()


async def buy_confirm_orders(schema, user) -> User:
    async with in_transaction():
        orders = await Order.filter(status=OrderStatus.IN_CART, user=user).all()
        if len(orders) <= 0:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Empty cart")

        summa = await get_summa_orders_cart(orders)
        new_balance_user = user.balance - summa

        if new_balance_user < 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough money")

        user.balance = new_balance_user
        await user.save()
        await update_status_and_address(orders, schema.address)

    return user


async def get_all_orders(user) -> list:
    return await Order.filter(user=user).all()
