import datetime
from typing import List, Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field

from src.items.constants import MAX_LIMIT_ITEMS


class UpdateItemSchema(BaseModel):
    id: int
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    discount_price: Optional[int] = None


class LastItemsSchema(BaseModel):
    offset: int = 0
    limit: int = MAX_LIMIT_ITEMS


class ParametersSchema(BaseModel):
    brand: Optional[str]
    material: Optional[str] = None
    size: Optional[str] = None
    country_creator: Optional[str] = None
    color: Optional[str] = None
    weight: Optional[str] = None
    height: Optional[float] = None
    width: Optional[float] = None
