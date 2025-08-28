import datetime
import random

from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from starlette import status

from src.cart.cart_service import get_cart_all, add_cart_item, remove_cart_item, clear_cart
from src.orders.models import Order, OrderStatus
from src.cart.schemas import AddOrderCartSchema
from src.models import User
from src.session.depends import validate_access_token
from src.utils import response

cart_router = APIRouter(prefix="/cart", tags=["Cart"])


@cart_router.get("/all")
async def all_handler(user: User = Depends(validate_access_token)):
    cart_items = await get_cart_all(user)
    return response(status=status.HTTP_200_OK, data=cart_items)


@cart_router.post("/add")
async def add_handler(schema: AddOrderCartSchema):
    new_cart_item = await add_cart_item(schema)
    return response(status=status.HTTP_204_NO_CONTENT,
                    data={"added": new_cart_item})


@cart_router.delete("/remove/{id}")
async def remove_handler(id: int, user: User = Depends(validate_access_token)):
    await remove_cart_item(id)
    return response(status=status.HTTP_204_NO_CONTENT,
                    message="Removed")


@cart_router.get("/clear")
async def clear_handler(user: User = Depends(validate_access_token)):
    await clear_cart(user)
    return response(status=status.HTTP_204_NO_CONTENT,
                    message="Clear")
