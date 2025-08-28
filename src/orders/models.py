from enum import IntEnum
from enum import Enum, IntEnum
from tortoise import fields, Model


class OrderStatus(IntEnum):
    IN_CART = 0
    WAITING = 1
    CONFIRM = 2
    CLOSED = 3
    IN_TRANSIT = 4
    READY = 5


class Order(Model):
    id = fields.IntField(generated=True, pk=True)
    date_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)

    delivery_date = fields.DateField(null=True)
    delivery_address = fields.CharField(max_length=256)
    status = fields.IntEnumField(OrderStatus)

    user = fields.ForeignKeyField("models.User", related_name="orders_bought")
    seller = fields.ForeignKeyField("models.User", related_name="orders_sold")
    item = fields.ForeignKeyField("models.Item", null=True)
    params = fields.JSONField(null=True)
