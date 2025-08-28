from tortoise import fields, Model


class Question(Model):
    id = fields.IntField(pk=True, generated=True)
    date_at = fields.DatetimeField(auto_now_add=True)
    item = fields.IntField()
    user = fields.ForeignKeyField("models.User")
    text = fields.CharField(max_length=512)

