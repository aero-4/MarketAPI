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


async def update_status(orders) -> None:
    for o in orders:
        o.status = OrderStatus.WAITING
        await o.save()


async def confirm_orders(user) -> User:
    async with in_transaction():
        await Order.create(
            user=user,
            status=OrderStatus.IN_CART
        )
        orders = await Order.filter(status=OrderStatus.IN_CART, user=user).all()
        if len(orders) <= 0:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Empty cart")

        summa = await get_summa_orders_cart(orders)
        new_balance_user = user.balance - summa

        if new_balance_user < 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough money")

        user.balance = new_balance_user
        await user.save()
        await update_status(orders)

    return user


async def get_all_orders(user):
    return await Order.filter(user=user).all()
