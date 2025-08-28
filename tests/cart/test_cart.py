import random
from types import SimpleNamespace

import pytest

from src.models import User, UserRoles
from src.items.models import Item
from src.orders.models import Order, OrderStatus
from src.cart import cart_service
from src.exceptions import NotFound, AlreadyExist


@pytest.mark.asyncio
async def test_add_and_get_cart_item():
    # подготовка: продавец, покупатель, товар
    seller = await User.create(phone=random.randint(10**10, 10**11 - 1), role=UserRoles.SELLER)
    print(seller)

    buyer = await User.create(phone=random.randint(10**10, 10**11 - 1), role=UserRoles.USER)
    item = await Item.create(
        article_id=random.randint(1, 10**6),
        title="Test item",
        description="desc",
        price=100,
        cat="cat",
        sub_cat="sub",
        params={},
        seller=seller,
    )
    print(buyer)

    # вызываем сервис добавления
    schema = SimpleNamespace(user=buyer, item=item.id, params={"count": 1})
    new_order = await cart_service.add_cart_item(schema)

    assert isinstance(new_order, Order)
    assert new_order.user_id == buyer.id or getattr(new_order, "user", None) == buyer.id
    assert new_order.item_id == item.id or getattr(new_order, "item", None) == item.id
    # seller в заказе должен совпадать с seller товара
    assert new_order.seller_id == seller.id or getattr(new_order, "seller", None) == seller.id
    assert new_order.status == OrderStatus.IN_CART

    # get_cart_all возвращает список dict'ов с нашим заказом
    cart_list = await cart_service.get_cart_all(buyer)
    assert isinstance(cart_list, list)
    assert len(cart_list) >= 1
    # проверим, что среди returned есть наш item id
    found = any(int(d.get("item") or d.get("item_id") or d.get("item_id")) == item.id for d in cart_list)
    assert found


@pytest.mark.asyncio
async def test_add_cart_item_already_exists_raises():
    seller = await User.create(phone=random.randint(10**10, 10**11 - 1), role=UserRoles.SELLER)
    buyer = await User.create(phone=random.randint(10**10, 10**11 - 1), role=UserRoles.SELLER)
    item = await Item.create(
        article_id=random.randint(1, 10**6),
        title="Exist item",
        description="desc",
        price=50,
        cat="cat",
        sub_cat="sub",
        params={},
        seller=seller,
    )

    # создаём существующий заказ вручную
    await Order.create(user=buyer, item=item, seller_id=seller.id, params={}, status=OrderStatus.IN_CART)

    schema = SimpleNamespace(user=buyer.id, item=item.id, params={})
    with pytest.raises(AlreadyExist):
        await cart_service.add_cart_item(schema)


@pytest.mark.asyncio
async def test_remove_cart_item_and_not_found():
    seller = await User.create(phone=random.randint(10**10, 10**11 - 1), role=UserRoles.SELLER)
    buyer = await User.create(phone=random.randint(10**10, 10**11 - 1), role=UserRoles.SELLER)
    item = await Item.create(
        article_id=random.randint(1, 10**6),
        title="Delete item",
        description="desc",
        price=10,
        cat="cat",
        sub_cat="sub",
        params={},
        seller=seller,
    )

    order = await Order.create(user=buyer, item=item, seller_id=seller.id, params={}, status=OrderStatus.IN_CART)

    # удаляем существующий
    await cart_service.remove_cart_item(order.id)
    assert await Order.get_or_none(id=order.id) is None

    # удаляем несуществующий -> NotFound
    with pytest.raises(NotFound):
        await cart_service.remove_cart_item(999999999)


@pytest.mark.asyncio
async def test_clear_cart_removes_all():
    seller = await User.create(phone=random.randint(10**10, 10**11 - 1), role=UserRoles.SELLER)
    buyer = await User.create(phone=random.randint(10**10, 10**11 - 1), role=UserRoles.SELLER)

    # создаём несколько товаров и заказов
    items = []
    for i in range(3):
        it = await Item.create(
            article_id=random.randint(1, 10**6),
            title=f"Clear item {i}",
            description="desc",
            price=5 * (i + 1),
            cat="cat",
            sub_cat="sub",
            params={},
            seller=seller,
        )
        items.append(it)
        await Order.create(user=buyer, item=it, seller_id=seller.id, params={}, status=OrderStatus.IN_CART)

    # проверим что есть заказы
    before = await Order.filter(user=buyer, status=OrderStatus.IN_CART).all()
    assert len(before) == 3

    # очищаем корзину
    await cart_service.clear_cart(buyer)

    after = await Order.filter(user=buyer, status=OrderStatus.IN_CART).all()
    assert len(after) == 0
