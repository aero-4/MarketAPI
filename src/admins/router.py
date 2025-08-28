from fastapi import APIRouter, Depends, status

from src.admins import admin_service
from src.admins.admin_service import change_visible_item
from src.admins.depends import validate_admin_role
from src.admins.schema import EditRoleUserSchema, ChangeVisibleItemSchema
from src.utils import response

admin_router = APIRouter(prefix="/admins", tags=["Admin"])


@admin_router.put("/edit-role")
async def admin_edit_role(schema: EditRoleUserSchema, admin=Depends(validate_admin_role)):
    updated_user = await admin_service.edit_role_user(schema)
    return response(status.HTTP_200_OK,
                    message="Updated new role",
                    data={"id": updated_user.id, "role": updated_user.role})


@admin_router.post("/moderate")
async def admin_moderate_items(schema: ChangeVisibleItemSchema, admin=Depends(validate_admin_role)):
    updated_item = await change_visible_item(schema)
    return response(status.HTTP_200_OK,
                    message=f"Updated visible item",
                    data={"id": updated_item.id, "visible": updated_item.is_visible})
