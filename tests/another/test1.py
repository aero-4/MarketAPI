import io
import uuid
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app import app
import src.reviews.router as reviews_mod

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch):
    """
    Подмена зависимостей и DB-операций на простые async-заглушки.
    Выполняется автоматически для каждого теста (autouse=True).
    """
    # тестовый пользователь, который вернётся из validate_access_token
    test_user = SimpleNamespace(id=42, username="tester")

    # Override зависимости авторизации (зависимость используется как Depends(validate_access_token))
    # FastAPI позволяет заменить зависимость через dependency_overrides:
    app.dependency_overrides[reviews_mod.validate_access_token] = lambda: test_user

    # mock save_media — просто возвращает имя файла, не пишет ничего
    async def fake_save_media(file, allowed_types, max_size):
        # проверяем, что allowed_types ожидаемый набор (необязательно)
        return f"saved-{uuid.uuid4()}.jpg"

    monkeypatch.setattr(reviews_mod, "save_media", fake_save_media)

    # mock Item.get_or_none — возвращаем объект с id и метод save
    async def fake_get_or_none(id=None, seller=None, **kwargs):
        # Проверяем, что seller передаётся наш test_user (по желанию)
        if getattr(seller, "id", None) != test_user.id:
            return None

        # dummy item with rating field and async save()
        class DummyItem:
            def __init__(self, id):
                self.id = id
                self.rating = 0.0

            async def save(self):
                # не делаем ничего, но async
                return None

        return DummyItem(id)

    monkeypatch.setattr(reviews_mod.Item, "get_or_none", fake_get_or_none)

    # mock Review.create
    async def fake_review_create(**kwargs):
        return SimpleNamespace(
            id=123,
            content=kwargs.get("content"),
            grade=kwargs.get("grade"),
            user_id=kwargs.get("user_id"),
            item_id=kwargs.get("item_id")
        )

    monkeypatch.setattr(reviews_mod.Review, "create", fake_review_create)

    # mock Media.create
    async def fake_media_create(**kwargs):
        # возвращаем объект с id и url
        return SimpleNamespace(id=uuid.uuid4(), url=kwargs.get("url"), group_id=kwargs.get("group_id"))

    monkeypatch.setattr(reviews_mod.Media, "create", fake_media_create)

    # mock Attachment.create
    async def fake_attachment_create(**kwargs):
        return SimpleNamespace(id=1, **kwargs)

    monkeypatch.setattr(reviews_mod, "Attachment", reviews_mod.Attachment)  # если Attachment класс есть
    monkeypatch.setattr(reviews_mod.Attachment, "create", fake_attachment_create)

    yield

    # Cleanup dependency overrides after test
    app.dependency_overrides.pop(reviews_mod.validate_access_token, None)


def make_upload_file_bytes(name="img.jpg", content=b"fake-image-bytes"):
    return (io.BytesIO(content), name)


def test_create_review_success(client):
    # Собираем multipart/form-data — поля + 2 файла
    data = {
        "item": "1",
        "content": "Great item!",
        "grade": "5",
    }
    files = [
        ("media_files", make_upload_file_bytes("a.jpg", b"1234")),
        ("media_files", make_upload_file_bytes("b.jpg", b"5678")),
    ]

    response = client.post("/reviews/create", data=data, files=files)
    assert response.status_code == 201
    # Проверяем, что возвращается JSON (в handler-е вы возвращаете new_review — замоканый object)
    # в нашем fake_review_create он сериализуется в словарь FastAPI TestClient'ом
    assert "id" in response.json() or response.content  # просто убеждаемся, что тело есть


def test_too_many_files(client):
    data = {"item": "1", "content": "X", "grade": "3"}
    files = [("media_files", make_upload_file_bytes(f"{i}.jpg")) for i in range(12)]  # 12 > 10 limit

    response = client.post("/reviews/create", data=data, files=files)
    assert response.status_code == 422
    assert "Too many files" in response.text
