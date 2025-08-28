from pydantic import BaseModel, Field


class ChangeStatusItemSchema(BaseModel):
    item_id: int
    status: int