from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Item(Model):
    id = fields.IntField(pk=True, generated=True)
    date_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)

    is_visible = fields.BooleanField(default=False)
    article_id = fields.BigIntField(unique=True)

    seller = fields.ForeignKeyField('models.User')
    title = fields.CharField(max_length=512, null=True)
    slug = fields.CharField(max_length=512, null=True)
    description = fields.TextField()
    price = fields.IntField(default=0)
    discount_price = fields.IntField(default=0)
    cat = fields.CharField(max_length=128)
    sub_cat = fields.CharField(max_length=128)
    params = fields.JSONField(default=dict)
    rating = fields.FloatField(default=0.0)
    count_all = fields.IntField(default=0)


ItemOut = pydantic_model_creator(Item, name="ItemOut", exclude_readonly=True)

