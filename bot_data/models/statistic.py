from tortoise import fields
from tortoise.models import Model

from .mixins import AuthorIdMixin, ChannelIdMixin


class StatsChannel(ChannelIdMixin, Model):
    channel_id = fields.BigIntField(index=True)
    child_channel_id = fields.BigIntField(index=True, null=True)

    class Meta:
        unique_together = ("channel_id", "child_channel_id")

    authors: fields.ReverseRelation["Statistic"]


class Statistic(AuthorIdMixin, Model):
    author_id = fields.BigIntField(null=False, index=True)
    messages = fields.IntField(null=False)
    parent_channel = fields.ForeignKeyField(
        "models.StatsChannel", related_name="authors"
    )

    class Meta:
        unique_together = ("parent_channel", "author_id")
