import importlib
import json
import random
import types

import pytest

from src.payments.schemas import PaymentOut

payments_service = importlib.import_module("src.payments.payments_service")
importlib.reload(payments_service)


@pytest.mark.asyncio
async def test_payment_success():
    from src.items import items_service
    from src.models import User, UserRoles

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)

    await items_service.create_item(
        title=f"Smartphone 321321",
        seller=seller,
        description="desc3",
        price=30,
        discount_price=15,
        params=json.dumps({"brand": f"X4412"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=random.randint(1, 25),
    )
    schema = types.SimpleNamespace(
        amount=123321
    )
    payment = await payments_service.create_payment(schema, seller)

    assert isinstance(payment, PaymentOut)
    assert payment.status == "success"

    user = await User.get_or_none(id=seller.id)
    assert user.balance == 123321


@pytest.mark.asyncio
async def test_payment_pending():
    from src.items import items_service
    from src.models import User, UserRoles

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)

    await items_service.create_item(
        title=f"Smartphone 321321",
        seller=seller,
        description="desc3",
        price=30,
        discount_price=15,
        params=json.dumps({"brand": f"X4412"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=random.randint(1, 25),
    )
    schema = types.SimpleNamespace(
        amount=123321
    )
    payment = await payments_service.create_payment(schema, seller)

    assert isinstance(payment, PaymentOut)
    assert payment.status == "pending"
