import importlib
import json
import random
import pytest

from types import SimpleNamespace


@pytest.mark.asyncio
async def test_get_last_reviews_and_reply():
    # reload modules
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)
    reviews_service = importlib.import_module("src.reviews.reviews_service")
    importlib.reload(reviews_service)

    from src.models import User, UserRoles, Replies
    from src.reviews.models import Review

    from src.models import ObjectTypesReplies

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    item = await items_service.create_item(
        title="T2",
        seller=seller,
        description="desc2",
        price=20,
        discount_price=10,
        params=json.dumps({"brand": "Samsung"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=1,
    )

    # Create two reviews
    r1 = await reviews_service.create_review(item.id, 4, "text1", user)
    r2 = await reviews_service.create_review(item.id, 5, "text2", user)

    # use schema-like object for get_last_reviews
    schema = SimpleNamespace(item=item.id, offset=0, limit=10)
    last = await reviews_service.get_last_reviews(schema)
    assert isinstance(last, list)
    assert len(last) >= 2
    assert all(isinstance(x, Review) for x in last)

    # reply to a review
    reply_schema = SimpleNamespace(item=item.id, text="reply text", current=r1.id)
    reply = await reviews_service.reply_review(reply_schema, user)
    assert isinstance(reply, Replies)
    assert reply.object_type == ObjectTypesReplies.REVIEW_REPLY


@pytest.mark.asyncio
async def test_like_review_add_and_remove():
    # reload modules
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)
    reviews_service = importlib.import_module("src.reviews.reviews_service")
    importlib.reload(reviews_service)

    from src.models import User, UserRoles, Replies
    from src.models import Likes, ObjectTypesLikes

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    item = await items_service.create_item(
        title="T3",
        seller=seller,
        description="desc3",
        price=30,
        discount_price=15,
        params=json.dumps({"brand": "X"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=1,
    )

    review = await reviews_service.create_review(item.id, 5, "like test", user)

    # add like
    like_schema = SimpleNamespace(value=1, item=item.id, current=review.id, object_type=ObjectTypesLikes.REVIEW_LIKE)
    like = await reviews_service.like_review(like_schema, user)
    assert isinstance(like, Likes)

    # remove like
    remove_schema = SimpleNamespace(value=0, item=item.id, current=review.id, object_type="review-like")
    removed = await reviews_service.like_review(remove_schema, user)
    # After removal, Likes.get_or_none should be None
    from src.models import Likes as LikesModel
    l = await LikesModel.get_or_none(user=user, current_id=review.id, object_type=remove_schema.object_type)
    assert l is None
