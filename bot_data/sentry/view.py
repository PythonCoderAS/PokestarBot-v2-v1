import abc
import logging

import discord.ui
import sentry_sdk

from .hub import CustomHub
from .sentry import (
    tags_from_values,
    report_exception,
    context_from_user,
    context_from_guild,
)
from ..funcs import start_transaction_or_child

logger = logging.getLogger(__name__)


class SentryView(discord.ui.View, abc.ABC):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("timeout", 300)
        super().__init__(*args, **kwargs)
        self.hub: sentry_sdk.Hub = CustomHub(sentry_sdk.Hub.current)

    async def _scheduled_task(
        self, item: discord.ui.Item, interaction: discord.Interaction
    ):
        name = f"{type(self).__name__}  Interaction"
        item_name = "{Unnamed Item}"
        item_type = type(item).__name__
        if isinstance(item, discord.ui.Button):
            item_name = item.label or item_name
        elif isinstance(item, discord.ui.Select):
            item_name = item.placeholder or item_name
        with start_transaction_or_child(
            self.hub,
            name=name,
            op="view_interaction",
            description=name + f": {item_type}: {item_name}",
        ):
            return await super()._scheduled_task(item, interaction)

    async def on_error(
        self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction
    ) -> None:
        sentry_context = {
            **context_from_user(
                interaction.user,
                interaction.channel
                if isinstance(interaction.channel, discord.abc.GuildChannel)
                else None,
            ),
            **context_from_guild(interaction.guild),
        }
        logger.exception("Error on %r in view", item, exc_info=error)
        return report_exception(
            error,
            sentry_context,
            hub=self.hub,
            tag_data=tags_from_values(
                interaction.user,
                interaction.guild,
                interaction.channel,
                None,
            ),
        )

    def merge_views(self, view: "SentryView"):
        for item in view.children:
            self.add_item(item)
