from typing import Optional

from pydantic import BaseModel, Field


class WishSchema(BaseModel):
    user: int
    item: int
    cat: Optional[str] = None
