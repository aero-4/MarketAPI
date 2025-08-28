from src.exceptions import NotFound, AlreadyExist
from src.items.models import Item
from src.wish.models import Wish


async def get_wish_all(user, cat) -> list:
    wish_list = await Wish.filter(user=user, cat=cat).all()
    return wish_list


async def get_wish(schema, user) -> Wish:
    if not await Item.get_or_none(id=schema.item):
        raise NotFound(message="Item not found")

    wish = await Wish.get_or_none(item=schema.item, user=user, cat=schema.cat)
    if not wish:
        raise NotFound(message="Wish not found")

    return wish


async def add_wish(schema, user) -> Wish:
    wish = await Wish.get_or_none(user=user, item_id=schema.item, cat=schema.cat)
    if wish:
        raise AlreadyExist()

    wish = await Wish.create(
        user=user,
        item_id=schema.item,
        cat=schema.cat
    )

    return wish


async def delete_wish(schema, user) -> Wish:
    wish = await get_wish(schema, user)
    await wish.delete()
    return wish
