from src.admins.schema import EditRoleUserSchema, ChangeVisibleItemSchema
from src.exceptions import NotFound
from src.items.models import Item
from src.models import User


async def edit_role_user(schema: EditRoleUserSchema) -> User:
    user = await User.get_or_none(id=schema.user_id)
    if not user:
        raise NotFound()

    user.role = schema.role
    await user.save()

    return user


async def change_visible_item(schema: ChangeVisibleItemSchema) -> Item:
    item = await Item.get_or_none(id=schema.item_id)
    if not item:
        raise NotFound()

    item.is_visible = schema.visible
    await item.save()

    return item
