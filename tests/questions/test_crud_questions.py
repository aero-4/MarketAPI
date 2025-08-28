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
async def test_create_question_success():
    # reload modules
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)
    questions_service = importlib.import_module("src.questions.questions_service")
    importlib.reload(questions_service)

    # models
    from src.models import User, UserRoles
    from src.questions.models import Question

    # create seller and user
    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    # create item to attach question to
    item = await items_service.create_item(
        title="Q item",
        seller=seller,
        description="desc",
        price=10,
        discount_price=5,
        params=json.dumps({"brand": "Test"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=1,
    )

    schema = SimpleNamespace(item=item.id, text="Is this available?")
    question = await questions_service.create_question(schema, user)

    assert isinstance(question, Question)
    assert question.text == "Is this available?"
    assert question.user.id == user.id
    assert question.item == item.id


@pytest.mark.asyncio
async def test_get_last_questions():
    # reload modules
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)
    questions_service = importlib.import_module("src.questions.questions_service")
    importlib.reload(questions_service)

    from src.models import User, UserRoles
    from src.questions.models import Question

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    item = await items_service.create_item(
        title="Q item 2",
        seller=seller,
        description="desc2",
        price=20,
        discount_price=10,
        params=json.dumps({"brand": "X"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=1,
    )

    # create several questions
    q1 = await questions_service.create_question(SimpleNamespace(item=item.id, text="Q1"), user)
    q2 = await questions_service.create_question(SimpleNamespace(item=item.id, text="Q2"), user)
    q3 = await questions_service.create_question(SimpleNamespace(item=item.id, text="Q3"), user)

    schema = SimpleNamespace(item=item.id, offset=0, limit=10)
    last = await questions_service.get_last_questions(schema)

    assert isinstance(last, list)
    # Expect at least the three we created
    assert len(last) >= 3
    texts = [q.text for q in last]
    assert "Q1" in texts and "Q2" in texts and "Q3" in texts
