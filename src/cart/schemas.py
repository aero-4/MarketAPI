from pydantic import BaseModel


class AddOrderCartSchema(BaseModel):
    user: int
    item: int
    params: dict
