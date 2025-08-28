from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from starlette.responses import JSONResponse, Response
from tortoise.transactions import in_transaction

from src.models import Replies, Likes, ObjectTypesLikes, User
from src.questions.models import Question
from src.questions.questions_service import create_question, reply_question, get_last_questions, like_question
from src.questions.schemas import *
from src.questions.models import *
from src.session.depends import validate_access_token
from src.utils import response

question_router = APIRouter(prefix="/questions", tags=["Questions"])


@question_router.get("/last")
async def last_handler(schema: LastQuestionsSchema):
    last_questions = await get_last_questions(schema)
    return response(status_code=status.HTTP_201_CREATED,
                    data=last_questions)


@question_router.post("/create")
async def create_handler(schema: QuestionSchema, user=Depends(validate_access_token)):
    question = await create_question(schema, user)
    return response(status_code=status.HTTP_201_CREATED,
                    data={"question": question.id})


@question_router.post("/reply")
async def reply_handler(schema: ReplyQuestionSchema, user: User = Depends(validate_access_token)):
    reply = await reply_question(schema, user)
    return response(status_code=status.HTTP_201_CREATED,
                    data={"reply": reply.id})


@question_router.post("/like")
async def like_handler(schema: LikeQuestionSchema, user: User = Depends(validate_access_token)):
    like = await like_question(schema, user)
    return response(status_code=status.HTTP_201_CREATED,
                    data={"like": like.id})
