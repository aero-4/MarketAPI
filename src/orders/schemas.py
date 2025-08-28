from pydantic import BaseModel


class BuyOrdersSchema(BaseModel):
    address: str
