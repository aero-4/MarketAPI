from cachetools.func import lru_cache
from fastapi import APIRouter

from src.items.items_service import *
from src.sellers.depends import validate_seller_role
from src.items.schemas import LastItemsSchema, UpdateItemSchema
from src.models import User
from src.utils import response
from fastapi import File, Form, Depends, status, UploadFile
from typing import List, Dict, Any

items_router = APIRouter(prefix="/items", tags=["Items"])


@lru_cache(maxsize=1024)
def get_schema_cached(cat: str, sub: str) -> Dict[str, Any]:
    return validate_for_category(cat, sub).schema()


@items_router.get("/params/{cat}/{sub_cat}")
async def get_params_schema_handler(cat: str, sub_cat: str, seller=Depends(validate_seller_role)):
    return get_schema_cached(cat, sub_cat)


@items_router.post("/create")
async def create_item_handler(
        seller: User = Depends(validate_seller_role),
        title: str = Form(..., description="Item title"),
        description: str = Form(..., description="Item desc"),
        count_all: int = Form(..., description="Item count"),
        price: int = Form(..., description="Item price"),
        discount_price: int = Form(..., description="Item discount price"),
        media_files: List[UploadFile] = File(..., min_length=1, description="List media-files"),
        cat: str = Form(..., description="Item category"),
        sub_cat: str = Form(..., description="Item sub category"),
        params: str = Form(..., description="Params item as JSON string"),
):
    item = await create_item(seller=seller, title=title, description=description, count_all=count_all, price=price, discount_price=discount_price, media_files=media_files, cat=cat, sub_cat=sub_cat,
                             params=params)
    return response(status.HTTP_200_OK, message="Item created", data=item)


@items_router.delete("/remove/{id}")
async def item_remove(id: int, seller=Depends(validate_seller_role)):
    await remove_item(id, seller)
    return response(status.HTTP_200_OK, message="Removed")


@items_router.put("/update")
async def item_update(schema: UpdateItemSchema, seller=Depends(validate_seller_role)):
    update_schema = schema.model_dump(exclude_none=True)
    item = await update_item(update_schema, seller)
    return response(status.HTTP_200_OK, data=item)


@items_router.get("/get/{id}")
async def item_get(id: int):
    result = await get_item(id)
    return response(status.HTTP_200_OK, data=result)


@items_router.post("/last")
async def last_items_handler(schema: LastItemsSchema):
    result = await last_items(schema)
    return response(status.HTTP_200_OK, data=result)
