from tortoise import fields
from tortoise.models import Model

from src.payments.enums import PaymentStatus


class Payment(Model):
    id = fields.CharField(max_length=64, pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    user = fields.ForeignKeyField("models.User", null=False)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    provider_id = fields.CharField(max_length=128, null=True)
    idempotency_key = fields.CharField(max_length=128, null=True, unique=True)
    status = fields.CharEnumField(max_length=32, default=PaymentStatus.PENDING, enum_type=PaymentStatus)
