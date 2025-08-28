import importlib
import json

import pytest

from src.admins.schema import EditRoleUserSchema, ChangeVisibleItemSchema
from src.auth.enums import UserRoles
from src.items.models import Item
from src.models import User

admin_service = importlib.import_module("src.admins.admin_service")
importlib.reload(admin_service)


@pytest.mark.asyncio
async def test_admin_edit_role():
    phone = 78789787878

    user = await User.create(phone=phone)
    schema = EditRoleUserSchema(user_id=user.id, role=UserRoles.MODER)
    new_role_user = await admin_service.edit_role_user(schema)
    user2 = await User.get_or_none(phone=phone)

    assert new_role_user.role == user2.role


@pytest.mark.asyncio
async def test_admin_change_visible_item():
    phone = 78789787878

    user = await User.create(phone=phone)
    seller = await User.create(phone=123142141224, role=UserRoles.SELLER)

    item1 = await Item.create(title="I1", seller=seller, description="d", price=1, discount_price=1, params=json.dumps({}), cat="c", sub_cat="s", count_all=1, article_id=1)


    schema = ChangeVisibleItemSchema(item_id=item1.id, visible=True)
    new_item = await admin_service.change_visible_item(schema)

    assert new_item.is_visible is True

    schema2 = ChangeVisibleItemSchema(item_id=item1.id, visible=False)
    new_item2 = await admin_service.change_visible_item(schema)

    assert new_item2.is_visible is False
