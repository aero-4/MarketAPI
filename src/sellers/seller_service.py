from src.exceptions import NotFound, UnavailableStatus, NotPermissions
from src.orders.models import OrderStatus, Order

OPERATIONS = [OrderStatus.CLOSED, OrderStatus.IN_TRANSIT, OrderStatus.READY]


async def get_purchased_orders(seller) -> list:
    orders = await Order.filter(seller=seller, status=OrderStatus.WAITING)
    return orders


async def get_order(item_id, seller) -> Order:
    order = await Order.get_or_none(item_id=item_id, seller=seller)
    if not order:
        raise NotFound()

    return order


async def edit_status(schema, seller) -> Order:
    order = await get_order(schema.item_id, seller)
    check_sequence = schema.status < order.status

    if schema.status not in OPERATIONS or check_sequence:
        raise UnavailableStatus()

    order.status = schema.status
    await order.save()
    return order
