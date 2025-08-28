from fastapi import APIRouter, Depends, status

from src.models import User
from src.orders.orders_service import confirm_orders, get_all_orders
from src.session.depends import validate_access_token
from src.utils import response

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.get("/all")
async def orders_all_handler(user: User = Depends(validate_access_token)):
    return await get_all_orders(user)


@order_router.post("/confirm")
async def confirm_orders_handler(user: User = Depends(validate_access_token)):
    user = await confirm_orders(user)
    return response(status=status.HTTP_200_OK,
                    message="Operation confirm",
                    data={"balance": user.balance})
