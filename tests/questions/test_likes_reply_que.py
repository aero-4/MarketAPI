# tests/questions/test_questions_service.py
import importlib
import json
import random
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from starlette import status


# autouse fixture to clean DB after each test
@pytest.fixture(autouse=True)
async def clear_db():
    from src.items.models import Item
    from src.models import Media, Attachment, Likes, Replies
    from src.questions.models import Question

    yield
    await Attachment.all().delete()
    await Media.all().delete()
    await Likes.all().delete()
    await Replies.all().delete()
    await Question.all().delete()
    await Item.all().delete()


@pytest.mark.asyncio
async def test_reply_question():
    # reload modules
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)
    questions_service = importlib.import_module("src.questions.questions_service")
    importlib.reload(questions_service)

    from src.models import User, UserRoles
    from src.questions.models import Question
    from src.models import ObjectTypesReplies, Replies

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    item = await items_service.create_item(
        title="Q item 3",
        seller=seller,
        description="desc3",
        price=30,
        discount_price=15,
        params=json.dumps({"brand": "Y"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=1,
    )

    question = await questions_service.create_question(SimpleNamespace(item=item.id, text="Need info"), user)

    reply_schema = SimpleNamespace(item=item.id, text="Answer here", current=question.id)
    reply = await questions_service.reply_question(reply_schema, user)

    assert isinstance(reply, Replies)
    assert reply.current_id == question.id
    assert reply.object_type == ObjectTypesReplies.QUESTION_REPLY


@pytest.mark.asyncio
async def test_like_question_add_and_remove():
    # reload modules
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)
    questions_service = importlib.import_module("src.questions.questions_service")
    importlib.reload(questions_service)

    from src.models import User, UserRoles
    from src.questions.models import Question
    from src.models import Likes, ObjectTypesLikes

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    item = await items_service.create_item(
        title="Q item 4",
        seller=seller,
        description="desc4",
        price=40,
        discount_price=20,
        params=json.dumps({"brand": "Z"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=1,
    )

    question = await questions_service.create_question(SimpleNamespace(item=item.id, text="Like me"), user)

    # add like
    like_schema = SimpleNamespace(value=1, item=item.id, current=question.id, object_type=ObjectTypesLikes.QUESTION_LIKE)
    like = await questions_service.like_question(like_schema, user)
    assert isinstance(like, Likes)

    # remove like
    remove_schema = SimpleNamespace(value=0, item=item.id, current=question.id, object_type=ObjectTypesLikes.QUESTION_LIKE)
    removed = await questions_service.like_question(remove_schema, user)
    # ensure removal: Likes.get_or_none should be None
    l = await Likes.get_or_none(user=user, current_id=question.id, object_type=remove_schema.object_type)
    assert l is None


@pytest.mark.asyncio
async def test_like_question_remove_not_liked_raises():
    # reload modules
    questions_service = importlib.import_module("src.questions.questions_service")
    importlib.reload(questions_service)

    from src.models import User, UserRoles
    from src.models import ObjectTypesLikes

    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    # Attempt to remove a like that doesn't exist
    remove_schema = SimpleNamespace(value=0, item=12345, current=99999, object_type=ObjectTypesLikes.QUESTION_REPLY_LIKE)

    with pytest.raises(HTTPException) as excinfo:
        await questions_service.like_question(remove_schema, user)

    assert excinfo.value.status_code == status.HTTP_403_FORBIDDEN
