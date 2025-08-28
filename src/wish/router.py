from fastapi import APIRouter, Depends, status
from src.models import User
from src.session.depends import validate_access_token
from src.utils import response
from src.wish.schemas import WishSchema
from src.wish.wish_service import get_wish_all, add_wish, delete_wish

wish_router = APIRouter(prefix="/wish", tags=["Wish"])


@wish_router.post("/all")
async def all_handler(user: User = Depends(validate_access_token)):
    return await get_wish_all(user)


@wish_router.post("/add")
async def get_wish_list_handler(schema: WishSchema, user: User = Depends(validate_access_token)):
    wish = await add_wish(schema, user)
    return response(status=status.HTTP_200_OK,
                    data={"wish": wish})


@wish_router.delete("/delete")
async def edit_handler(schema: WishSchema, user: User = Depends(validate_access_token)):
    wish = await delete_wish(schema, user)
    return response(status=status.HTTP_200_OK,
                    data={"wish": wish},
                    message="deleted")
