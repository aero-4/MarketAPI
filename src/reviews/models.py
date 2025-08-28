from tortoise import fields, Model


class Review(Model):
    id = fields.IntField(pk=True, generated=True)
    date_at = fields.DatetimeField(auto_now_add=True)
    update_at = fields.DatetimeField(auto_now=True)

    item = fields.ForeignKeyField("models.Item")
    content = fields.CharField(max_length=512)
    user = fields.ForeignKeyField("models.User")
    media = fields.ForeignKeyField("models.Media", null=True)
    grade = fields.IntField(null=False)

    def __str__(self):
        return f"{self.id} {self.content} {self.user} {self.grade}"
