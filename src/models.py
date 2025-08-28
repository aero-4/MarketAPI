from tortoise import Model, fields

from src.auth.enums import UserRoles
from enum import Enum


class ObjectTypesReplies(str, Enum):
    REVIEW_REPLY = "review-reply"
    REVIEW = "review"
    QUESTION_REPLY = "question-reply"
    QUESTION = "question"


class ObjectTypesLikes(str, Enum):
    REVIEW_LIKE = "review-like"
    REVIEW_REPLY_LIKE = "review-reply-like"
    QUESTION_LIKE = "question-like"
    QUESTION_REPLY_LIKE = "question-reply-like"


class User(Model):
    id = fields.IntField(pk=True, generated=True)
    date_at = fields.DatetimeField(auto_now_add=True)
    first_name = fields.CharField(max_length=64, null=True)
    full_name = fields.CharField(max_length=64, null=True)
    photo = fields.TextField(null=True)
    email = fields.CharField(max_length=128, null=True)
    phone = fields.BigIntField(null=True)
    balance = fields.IntField(default=0)
    role = fields.IntField(default=UserRoles.USER.value)

    def __str__(self):
        return f'User: {self.id} / {self.phone}'


# class UserAddress(Model):
#     id = fields.IntField(pk=True, generated=True)
#     user = fields.ForeignKeyField("models.User")
#     address = fields.CharField(max_length=512)


class Media(Model):
    id = fields.IntField(pk=True, generated=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    group_id = fields.UUIDField(null=True, index=True)
    url = fields.CharField(max_length=512)


class RefreshToken(Model):
    id = fields.IntField(pk=True, generated=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)

    jti = fields.CharField(unique=True, index=True, max_length=64)
    user = fields.ForeignKeyField('models.User')
    revoked = fields.BooleanField(default=False)


class Likes(Model):
    id = fields.IntField(pk=True, generated=True)
    date_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User")
    item = fields.ForeignKeyField("models.Item")
    current_id = fields.IntField(null=False, unique=True)
    object_type = fields.CharEnumField(ObjectTypesLikes)
    value = fields.IntField(null=False)


class Replies(Model):
    id = fields.IntField(pk=True, generated=True)
    date_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User")
    item = fields.ForeignKeyField("models.Item")
    current_id = fields.IntField(null=False, unique=False)
    object_type = fields.CharEnumField(ObjectTypesReplies)
    content = fields.CharField(null=False, max_length=256)


class Attachment(Model):
    id = fields.IntField(pk=True, generated=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    media = fields.ForeignKeyField('models.Media', related_name='attachments')
    content_type = fields.CharField(max_length=50)
    object_id_int = fields.IntField(null=True)
    object_id_uuid = fields.UUIDField(null=True)

    class Meta:
        indexes = [("content_type", "object_id_int"), ("content_type", "object_id_uuid")]
