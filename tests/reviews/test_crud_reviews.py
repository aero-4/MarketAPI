import importlib
import json
import random
import pytest

from types import SimpleNamespace



# фикстура очистки БД — ваша версия
@pytest.fixture(autouse=True)
async def clear_db():
    from src.items.models import Item
    from src.models import Media, Attachment, Likes, Replies
    from src.reviews.models import Review

    yield
    await Attachment.all().delete()
    await Media.all().delete()
    await Likes.all().delete()
    await Replies.all().delete()
    await Item.all().delete()
    await Review.all().delete()


@pytest.mark.asyncio
async def test_create_review_success():
    # (re)load services to ensure fresh module state
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)
    reviews_service = importlib.import_module("src.reviews.reviews_service")
    importlib.reload(reviews_service)

    # models
    from src.models import User, UserRoles
    from src.reviews.models import Review

    # create seller and user
    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    # create item
    item = await items_service.create_item(
        title="T",
        seller=seller,
        description="desc",
        price=10,
        discount_price=5,
        params=json.dumps({"brand": "Iphone"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=1,
    )

    # create review
    review = await reviews_service.create_review(
        item.id,
        5,
        str(random.getrandbits(64) << 1),
        user
    )

    assert review.grade == 5
    assert isinstance(review, Review)


@pytest.mark.asyncio
async def test_create_review_item_not_found():
    # reload modules
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)
    reviews_service = importlib.import_module("src.reviews.reviews_service")
    importlib.reload(reviews_service)

    from src.models import User, UserRoles
    # create a user
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    fake_item_id = 999999999  # non-existent
    with pytest.raises(Exception) as excinfo:
        await reviews_service.create_review(
            fake_item_id,
            5,
            "bad item test",
            user
        )
    # Expect NotFound or HTTPException depending on implementation
    assert excinfo.type is not None


@pytest.mark.asyncio
async def test_get_edit_delete_review_cycle():
    # reload modules
    items_service = importlib.import_module("src.items.items_service")
    importlib.reload(items_service)
    reviews_service = importlib.import_module("src.reviews.reviews_service")
    importlib.reload(reviews_service)

    from src.models import User, UserRoles
    from src.reviews.models import Review

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.SELLER)
    user = await User.create(phone=random.randint(10000000000, 99999999999),
                             role=UserRoles.USER)

    item = await items_service.create_item(
        title="T4",
        seller=seller,
        description="desc4",
        price=40,
        discount_price=20,
        params=json.dumps({"brand": "Z"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=1,
    )

    # create review
    review = await reviews_service.create_review(item.id, 3, "orig content", user)

    # get_review
    got = await reviews_service.get_review(review.id, user)
    assert isinstance(got, Review)
    assert got.id == review.id

    # edit
    edit_schema = SimpleNamespace(id=review.id, content="edited content")
    edited = await reviews_service.edit_review(edit_schema, user)
    assert edited.content == "edited content"

    # delete
    deleted = await reviews_service.delete_review(review.id, user)
    # ensure it was deleted
    from src.reviews.models import Review as ReviewModel
    should_be_none = await ReviewModel.get_or_none(id=review.id)
    assert should_be_none is None
