import asyncio
import logging
import uuid
from pathlib import Path
from typing import List

from fastapi import HTTPException
from starlette import status
from tortoise.transactions import in_transaction

from src.exceptions import NotFound
from src.items.models import Item
from src.models import ObjectTypesReplies, Replies, Likes, ObjectTypesLikes, Media, Attachment
from src.questions.models import Question
from src.reviews.models import Review
from src.utils import update_object_media, save_media, response


async def get_last_reviews(schema) -> list:
    reviews = await (
        Review
        .filter(item=schema.item)
        .offset(schema.offset)
        .limit(schema.limit)
        .order_by("date_at")
        .all()
    )
    await update_object_media(reviews)
    return reviews


def add_grade(avg, count, r):
    new_count = count + 1
    new_avg = (avg * count * r) / new_count
    return round(new_avg, 1)


async def create_review(item_id, grade, content, user, media_files=None) -> Review:
    if media_files and len(media_files) > 10:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Too many files")

    if not (1 <= grade <= 5):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Grade must be 1..5")

    db_item = await Item.get_or_none(id=int(item_id))
    if not db_item:
        raise NotFound()

    saved_files_media: List[str] = await asyncio.gather(*[
        save_media(file) for file in media_files
    ]) if media_files and len(media_files) > 0 else []

    try:
        async with in_transaction():
            review = await Review.create(
                content=content,
                user_id=user.id,
                item_id=db_item.id,
                grade=grade,
            )
            group_id = uuid.uuid4()

            for file_name in saved_files_media:
                media = await Media.create(
                    group_id=group_id,
                    url=file_name
                )
                await Attachment.create(media_id=media.id, content_type="review", object_id_int=review.id)

            count_grades = await Review.filter(item_id=db_item.id).count()
            db_item.rating = add_grade(db_item.rating, count_grades, grade)
            await db_item.save()


    except Exception as e:
        logging.error(e)

        for file_name in saved_files_media:
            try:
                Path("files", file_name).unlink()
            except Exception:
                pass
        raise HTTPException(status_code=500, detail="DB error while creating review")

    return review


async def reply_review(schema, user) -> Replies:
    reply = await Replies.create(
        item_id=schema.item,
        user=user,
        content=schema.text,
        current_id=schema.current,
        object_type=ObjectTypesReplies.REVIEW_REPLY
    )
    return reply


async def like_review(schema, user) -> Likes:
    async with in_transaction():
        if schema.value == 0:
            like = await Likes.get_or_none(user=user, current_id=schema.current, object_type=schema.object_type)
            if not like:
                raise NotFound()

            await like.delete()

        else:
            like, created = await Likes.update_or_create(
                defaults={"value": schema.value, "object_type": schema.object_type},
                item_id=schema.item,
                user=user,
                current_id=schema.current,
            )
    return like


async def get_review(id, user):
    review = await Review.get_or_none(id=id, user=user)
    if not review:
        raise NotFound(message="Review not found")
    return review


async def delete_review(id, user) -> Review:
    review = await get_review(id, user)
    await review.delete()
    return review


async def edit_review(schema, user) -> Review:
    review = await get_review(schema.id, user)
    review.content = schema.content
    await review.save()
    return review
