from tortoise import fields, Model


class Wish(Model):
    id = fields.IntField(pk=True, generated=True)
    date_at = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField("models.User")
    item = fields.ForeignKeyField("models.Item")
    cat = fields.CharField(max_length=32, null=True)
