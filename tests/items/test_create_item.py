import importlib
import json
import random

import pytest
from fastapi import HTTPException

from src.auth.enums import UserRoles
from src.items.models import Item
from src.models import User


@pytest.fixture(autouse=True)
async def clear_db():
    from src.items.models import Item
    from src.models import Media, Attachment

    yield
    await Attachment.all().delete()
    await Media.all().delete()
    await Item.all().delete()


class DummyUploadFile:
    def __init__(self, filename, content_type, data=b"ok"):
        self.filename = filename
        self.content_type = content_type
        self._data = data
        self._pos = 0

    async def read(self, n=-1):
        if self._pos >= len(self._data):
            return b""
        if n == -1:
            n = len(self._data) - self._pos
        chunk = self._data[self._pos:self._pos + n]
        self._pos += len(chunk)
        return chunk


@pytest.mark.asyncio
async def test_create_item_success(monkeypatch):
    item_service = importlib.import_module("src.items.items_service")
    importlib.reload(item_service)

    async def fake_save_media(file):
        return f"stored/{getattr(file, 'filename', 'file')}"

    monkeypatch.setattr(item_service, "save_media", fake_save_media, raising=True)
    monkeypatch.setattr(item_service, "create_slug", lambda t: "slug-" + t, raising=False)

    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.USER)
    files = [DummyUploadFile("a.jpg", "image/png"), DummyUploadFile("b.mp4", "video/mp4")]

    item = await item_service.create_item(
        title="T",
        seller=seller,
        description="desc",
        price=10,
        discount_price=5,
        params=json.dumps({"brand": "Iphone"}),
        cat="electronics",
        sub_cat="smartphone",
        count_all=1,
        media_files=files
    )

    db_item = await Item.get_or_none(id=item.id)
    assert db_item is not None


@pytest.mark.asyncio
async def test_not_valid_category(monkeypatch):
    item_service = importlib.import_module("src.items.items_service")
    importlib.reload(item_service)

    async def fake_save_media(file):
        return f"stored/{getattr(file, 'filename', 'file')}"

    monkeypatch.setattr(item_service, "save_media", fake_save_media, raising=True)
    monkeypatch.setattr(item_service, "create_slug", lambda t: "slug-" + t, raising=False)



    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.USER)
    files = [DummyUploadFile("a.jpg", "image/png"), DummyUploadFile("b.mp4", "video/mp4")]
    with pytest.raises(HTTPException) as exinfo:
        item = await item_service.create_item(
            title="T",
            seller=seller,
            description="desc",
            price=10,
            discount_price=5,
            params=json.dumps({"brand": "Iphone"}),
            cat="123",
            sub_cat="123",
            count_all=1,
            media_files=files
        )
    assert exinfo.value.status_code == 400
    assert exinfo.value.detail == [{'loc': ['cat'], 'msg': "Unknown category '123'", 'type': 'value_error'}]


@pytest.mark.asyncio
async def test_empty_media_files(monkeypatch):
    item_service = importlib.import_module("src.items.items_service")
    importlib.reload(item_service)

    async def fake_save_media(file):
        return f"stored/{getattr(file, 'filename', 'file')}"

    monkeypatch.setattr(item_service, "save_media", fake_save_media, raising=True)
    monkeypatch.setattr(item_service, "create_slug", lambda t: "slug-" + t, raising=False)
    seller = await User.create(phone=random.randint(10000000000, 99999999999),
                               role=UserRoles.USER)
    files = []

    with pytest.raises(HTTPException) as exinfo:
        item = await item_service.create_item(
            title="T",
            seller=seller,
            description="desc",
            price=10,
            discount_price=5,
            params=json.dumps({"brand": "Iphone"}),
            cat="123",
            sub_cat="123",
            count_all=1,
            media_files=files
        )
        print(exinfo)
        assert exinfo.value.status_code == 405

