import logging

from tortoise.exceptions import OperationalError
from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from src.items.models import Item
from src.search.schemas import SearchResultSchema, SearchSchema

logger = logging.getLogger(__name__)


async def search_last_items(schema: SearchSchema):
    try:
        filters = {}

        if schema.params:
            filters["params__contains"] = schema.params

        if schema.cat:
            filters["cat__contains"] = schema.cat

        if schema.sub_cat:
            filters["sub_cat__contains"] = schema.sub_cat

        qs = Item.filter(**filters)

        if schema.query:
            qs = qs.filter(
                Q(title__icontains=schema.query) |
                Q(description__icontains=schema.query) |
                Q(slug__icontains=schema.query)
            )

        items = await qs.offset(schema.offset).limit(schema.limit + 1).all().values()
        has_more = len(items) > schema.limit

        return SearchResultSchema(
            data=items,
            limit=schema.limit,
            offset=schema.offset,
            has_more=has_more,
        )

    except OperationalError as e:
        logger.exception("DB operation failed")
        raise e

    except Exception as e:
        logger.exception("Unexpected error in search")
        raise e
