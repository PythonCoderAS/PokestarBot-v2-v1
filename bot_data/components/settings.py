import asyncio
from typing import Dict, ClassVar, Any, Type, Iterator

import discord.ext.commands

from . import Component
from .orm import ORM
from ..funcs import GuildSetting, AttrDict
from ..models import GlobalOption


class SuffixString(str):
    """A string, which is a prefix. Returns a string that is a suffix."""

    def reversed(self) -> str:
        return self[::-1].replace("(", ")").replace("[", "]").replace("{", "}")

    def __reversed__(self) -> Iterator[str]:
        return iter(self.reversed())

    @property
    def reversed_string(self):
        return self.reversed()


class BotSettings(AttrDict):
    __slots__ = ()

    command_name_markdown: SuffixString
    command_name_markdown_sep: str
    base_domain: str
    redirect_url: str
    timezone: str
    glossary_markdown_sep: str
    discord_api_base: str
    glossary_markdown: SuffixString
    open_weather_api_base: str
    webserver_ip: str
    owner_id: int
    webserver_port: int
    flag_prefix: str
    flag_delimiter: str

    transformation_data: ClassVar[Dict[str, Type[Any]]] = {
        "owner_id": int,
        "webserver_port": int,
        "command_name_markdown": SuffixString,
        "glossary_markdown": SuffixString,
    }

    def __setitem__(self, k, v):
        if k in self.transformation_data:
            v = self.transformation_data[k](v)
        super().__setitem__(k, v)

    @property
    def items_to_init(self):
        acceptable_types = (str, *set(self.transformation_data.values()))
        return {
            item
            for item, val in self.__annotations__.items()
            if isinstance(val, type) and issubclass(val, acceptable_types)
        }

    def __repr__(self) -> str:
        return dict.__repr__(self.data)


class Settings(Component):
    """Deals with bot and guild settings."""

    set_as = "settings"

    require = [ORM]

    def __init__(self, bot):
        super().__init__(bot)
        self.bot_settings: BotSettings = BotSettings()
        self._on_message = self.bot.on_message
        self.on_ready_load = asyncio.Event()
        self._prefix = self.bot.command_prefix

    async def load_bot_settings(self):
        async for item in GlobalOption.all():
            self.bot_settings[item.name] = item.value

    async def init_async(self):
        await self.load_bot_settings()
        if self.bot_settings.get("owner_id", None):
            self.bot.owner_id = self.bot_settings.owner_id

    async def stop_async(self):
        await self.save_global_options()
        del self.bot.on_guild_join
        self.bot.command_prefix = self._prefix

    async def save_global_options(self):
        await asyncio.gather(
            *[
                GlobalOption.update_or_create(dict(value=str(val)), name=name)
                for name, val in self.bot_settings.items()
            ]
        )

    def get_absolute_url_from_relative(self, path: str):
        return self.bot_settings.base_domain + path
