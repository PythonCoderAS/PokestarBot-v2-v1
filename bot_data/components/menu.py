from typing import MutableMapping

import cachetools
import discord

from . import Component
from ..funcs import start_transaction_or_child
from ..menu import Menu


class MenuComponent(Component):
    """A component storing all of the bot's menu data."""

    set_as = "menu"

    def __init__(self, bot):
        super().__init__(bot)
        self.menus: MutableMapping[int, Menu] = cachetools.TTLCache(
            30,
            60 * 5,
        )
        self._old_raw_reaction_add = None

    async def init_async(self):
        on_raw_reaction_add = self.on_raw_reaction_add
        if hasattr(self.bot, "on_raw_reaction_add"):
            self._old_raw_reaction_add = self.bot.on_raw_reaction_add

            async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
                await self.on_raw_reaction_add(payload)
                await self._old_raw_reaction_add(payload)

        self.bot.on_raw_reaction_add = on_raw_reaction_add

    async def stop_async(self):
        if self._old_raw_reaction_add is None:
            del self.bot.on_raw_reaction_add
        else:
            self.bot.on_raw_reaction_add = self._old_raw_reaction_add

    async def post_menu(
        self, channel: discord.abc.Messageable, menu: Menu
    ) -> discord.Message:
        """Post the menu and save it in the bot cache."""
        msg = await menu.post_menu(channel)
        if menu:
            self.menus[msg.id] = menu
        return msg

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        if payload.message_id in self.menus:
            menu = self.menus[payload.message_id]
            if menu:
                with start_transaction_or_child(
                    name="Reaction", op="reaction", description="Reaction"
                ) as span:
                    span.set_tag("emoji", str(payload.emoji))
                    return await menu.execute_reaction(payload)
