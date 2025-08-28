from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form
from starlette import status
from src.models import User
from src.reviews.reviews_service import get_last_reviews, reply_review, like_review, delete_review, edit_review, create_review
from src.reviews.schemas import *
from src.session.depends import validate_access_token
from src.utils import response

reviews_router = APIRouter(prefix="/reviews", tags=["Reviews"])


@reviews_router.post("/create")
async def create_handler(
        item: int = Form(...),
        content: str = Form(...),
        grade: int = Form(...),
        media_files: List[UploadFile] = File(None,
                                             description="List media-files - review max length = 10"),
        user: User = Depends(validate_access_token),
):
    review = await create_review(item, grade, content, media_files, user)
    return response(status.HTTP_201_CREATED,
                    data=review)


@reviews_router.patch("/edit")
async def edit_handler(schema: EditReviewSchema, user: User = Depends(validate_access_token)):
    review = await edit_review(schema, user)
    return response(status.HTTP_200_OK,
                    data=review)


@reviews_router.post("/last")
async def last_handler(schema: LastReviewsSchema):
    reviews = await get_last_reviews(schema)
    return response(status.HTTP_200_OK,
                    data=reviews)


@reviews_router.delete("/delete/{id}")
async def delete_handler(id: int, user=Depends(validate_access_token)):
    review = await delete_review(id, user)
    return response(status.HTTP_200_OK,
                    data=review,
                    message="deleted")


@reviews_router.post("/reply")
async def reply_handler(schema: ReplyReviewSchema, user: User = Depends(validate_access_token)):
    reply = await reply_review(schema, user)
    return response(status.HTTP_200_OK,
                    data=reply)


@reviews_router.post("/like")
async def reply_handler(schema: LikeReviewSchema, user: User = Depends(validate_access_token)):
    like = await like_review(schema, user)
    return response(status.HTTP_200_OK,
                    data=like)
