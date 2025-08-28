from fastapi import HTTPException
from starlette import status
from tortoise.transactions import in_transaction

from src.models import ObjectTypesReplies, Replies, Likes
from src.questions.models import Question


async def get_last_questions(schema) -> list:
    questions = await (
        Question.
        filter(item=schema.item).
        offset(schema.offset).
        limit(schema.limit).
        order_by("date_at").
        all()
    )
    return questions


async def create_question(schema, user) -> Question:
    question = await Question.create(
        item=schema.item,
        text=schema.text,
        user=user,
    )
    return question


async def reply_question(schema, user) -> Replies:
    reply = await Replies.create(
        item_id=schema.item,
        user=user,
        content=schema.text,
        current_id=schema.current,
        object_type=ObjectTypesReplies.QUESTION_REPLY
    )
    return reply


async def like_question(schema, user) -> Likes:
    async with in_transaction():
        if schema.value == 0:
            like = await Likes.get_or_none(user=user, current_id=schema.current, object_type=schema.object_type)
            if not like:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not liked")

            await like.delete()
        else:
            like, created = await Likes.update_or_create(
                defaults={"value": schema.value, "object_type": schema.object_type},
                item_id=schema.item,
                user=user,
                current_id=schema.current,
            )
    return like

