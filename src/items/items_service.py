import asyncio
import json
import random
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, ValidationError
from starlette import status
from tortoise.expressions import RawSQL
from tortoise.transactions import in_transaction

from src.exceptions import NotFound
from src.items.constants import MAX_LIMIT_SIMILAR, MAX_LIMIT_ITEMS, CATEGORIZED_PARAMS_SCHEMAS
from src.items.models import Item
from src.items.schemas import ParametersSchema
from src.models import Media, Attachment
from src.search.schemas import SearchResultSchema
from src.utils import save_media, create_slug, update_object_media


def validate_for_category(cat: str, sub_cat: str):
    model_cls = CATEGORIZED_PARAMS_SCHEMAS.get(cat.lower())
    if not model_cls:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"loc": ["cat"], "msg": f"Unknown category '{cat}'", "type": "value_error"}]
        )
    model_cls = model_cls.get(sub_cat.lower())
    if not model_cls:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"loc": ["cat"], "msg": f"Unknown sub-category '{sub_cat}'", "type": "value_error"}]
        )
    return model_cls


def validate_params_for_category(cat: str, sub_cat: str, params_json: str) -> BaseModel:
    validate_for_category(cat, sub_cat)
    try:
        raw = json.loads(params_json)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[{"loc": ["params"], "msg": "Invalid JSON params", "type": "value_error.json"}]
        )
    try:
        return ParametersSchema(**raw)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.errors()
        )


async def create_item(*, title, seller, description, price, discount_price, params, cat, sub_cat, count_all, media_files: list = None) -> Item:
    saved_files = await asyncio.gather(*[save_media(file) for file in media_files]) if media_files and len(media_files) > 0 else []

    async with in_transaction() as tx:
        valid_params = validate_params_for_category(cat, sub_cat, params)

        rand_article_id = random.randint(1_000_00, 9_999_999)
        item = await Item.create(
            slug=create_slug(title),
            article_id=rand_article_id,
            seller_id=seller.id,
            title=title,
            description=description,
            price=price,
            discount=discount_price,
            params=valid_params,
            cat=cat,
            sub_cat=sub_cat,
            count_all=count_all,
            using_db=tx
        )
        group_id = uuid.uuid4()

        for file_name in saved_files:
            media = await Media.create(
                group_id=group_id,
                url=file_name,
                using_db=tx
            )
            await Attachment.create(media_id=media.id, content_type="item", object_id_int=item.id, using_db=tx
)
        return item


async def remove_item(id: int, seller_id: int) -> None:
    item = await Item.get_or_none(id=id, seller_id=seller_id)
    if not item:
        raise NotFound()
    removed = await item.delete()
    return removed


async def update_item(schema, seller_id: int):
    update = {
        "title": schema.title,
        "description": schema.description,
        "price": schema.price,
    }
    return await Item.filter(id=schema.id, seller_id=seller_id).update(**update)


async def get_item(id: int) -> dict:
    item = await Item.get_or_none(id=id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item_dict = await Item.filter(id=item.id).first().values()

    similar = await (
        Item
        .filter(cat=item.cat, sub_cat=item.sub_cat)
        .exclude(id=item.id)
        .annotate(random_order=RawSQL("RANDOM()"))
        .order_by("random_order")
        .limit(MAX_LIMIT_SIMILAR)
    ).values()

    await update_object_media([item_dict])
    await update_object_media(similar)

    return {"item": item_dict, "similar_items": similar}


async def last_items(schema) -> SearchResultSchema:
    qs = Item.filter()
    limit = min(schema.limit or MAX_LIMIT_ITEMS, MAX_LIMIT_ITEMS)
    items = await qs.offset(schema.offset).limit(limit + 1).order_by("date_at").all().values()
    has_more = len(items) > limit
    await update_object_media(items)

    return SearchResultSchema(
        data=items,
        limit=limit,
        offset=schema.offset,
        has_more=has_more,
    )
