from typing import Optional

from pydantic import BaseModel, Field, validator, field_validator

from src.models import ObjectTypesLikes, ObjectTypesReplies


class QuestionSchema(BaseModel):
    text: str = Field(..., max_length=256)
    item: int


class ReplyQuestionSchema(BaseModel):
    text: str = Field(..., max_length=256)
    item: int
    current: int



class LastQuestionsSchema(BaseModel):
    item: int
    offset: int
    limit: int


class LikeQuestionSchema(BaseModel):
    item: int
    value: int
    current: int
    object_type: ObjectTypesLikes

    @field_validator("value", mode="before")
    def value_must_be_allowed(cls, v):
        if v not in (1, -1, 0):
            raise ValueError("value must be one of: 1, -1, 0")
        return v
