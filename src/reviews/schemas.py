from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.models import ObjectTypesLikes


class ReviewSchema(BaseModel):
    item: int
    content: str = Field(..., max_length=512)
    media: Optional[int] = None
    grade: int = Field(..., le=5, ge=1)


class EditReviewSchema(BaseModel):
    id: int
    content: str = Field(..., max_length=512)


class ReplyReviewSchema(BaseModel):
    item: int
    content: str = Field(..., max_length=256)
    current: int


class LastReviewsSchema(BaseModel):
    item: int
    offset: int
    limit: int


class LikeReviewSchema(BaseModel):
    item: int
    value: int
    current: int
    object_type: ObjectTypesLikes

    @field_validator("value", mode="before")
    def value_must_be_allowed(cls, v):
        if v not in (1, -1, 0):
            raise ValueError("value must be one of: 1, -1, 0")
        return v
