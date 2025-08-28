from fastapi import APIRouter, Depends

from src.exceptions import NotFound
from src.sellers.depends import validate_seller_role
from src.sellers.schemas import ChangeStatusItemSchema

from src.sellers.seller_service import edit_status, get_purchased_orders
from src.utils import response

seller_router = APIRouter(prefix="/sellers", tags=["Sellers"])


@seller_router.get("/purchased/all")
async def purchased_handler(seller=Depends(validate_seller_role)):
    purchased_orders = await get_purchased_orders(seller)
    return response(data=purchased_orders)


@seller_router.patch("/purchased/status/change", description="-1 - close item, 3 - in transit, 4 - ready")
async def change_purchased_status_handler(schema: ChangeStatusItemSchema, seller=Depends(validate_seller_role)):
    changed_status_order = await edit_status(schema, seller)
    return response(data=changed_status_order,
                    message="changed status")
