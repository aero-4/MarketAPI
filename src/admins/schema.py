from typing import Optional

from pydantic import BaseModel, Field

from src.auth.enums import UserRoles


class EditRoleUserSchema(BaseModel):
    user_id: Optional[int]
    role: Optional[int] = Field(..., ge=UserRoles.USER.value, le=UserRoles.ADMIN.value)


class ChangeVisibleItemSchema(BaseModel):
    item_id: int
    visible: bool
