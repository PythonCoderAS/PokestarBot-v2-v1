import asyncio
import dataclasses
from typing import (
    Dict,
    List,
    Optional,
    TYPE_CHECKING,
    Union,
)

import discord.ext.commands

from .response import Response
from ..models import (
    BotSpamCommand,
    DisabledCommand,
    NamedChannel,
    Option,
    Prefix,
    NamedRole,
)
from ..setup import setup_constants

if TYPE_CHECKING:
    from ..bot import PokestarBot


@dataclasses.dataclass()
class GuildSetting:
    bot: "PokestarBot"
    guild_id: int
    channels: Dict[str, int] = dataclasses.field(default_factory=dict)
    options: Dict[str, bool] = dataclasses.field(default_factory=dict)
    banned_commands: List[str] = dataclasses.field(default_factory=list)
    restricted_commands: List[str] = dataclasses.field(default_factory=list)
    prefix: str = "%"
    roles: Dict[str, int] = dataclasses.field(default_factory=dict)

    def get_channel(
        self, name: str, follow: bool = True
    ) -> Optional[
        Union[
            discord.TextChannel,
            discord.VoiceChannel,
            discord.CategoryChannel,
            discord.StageChannel,
        ]
    ]:
        if name not in self.channels:
            fallback = setup_constants["Channels"][name].fallback_channel
            if fallback and follow:
                return self.get_channel(fallback)
            else:
                return None
        else:
            return self.bot.get_channel(self.channels[name])

    def get_option(self, name: str) -> bool:
        if name not in self.options:
            return setup_constants["Options"][name].default
        return self.options[name]

    async def set_channel(self, name: str, value: int):
        await NamedChannel.update_or_create(
            channel_name=name, guild_id=self.guild_id, defaults=dict(channel_id=value)
        )
        self.channels[name] = value

    async def set_option(self, name: str, value: bool):
        await Option.update_or_create(
            dict(enabled=value), name=name, guild_id=self.guild_id
        )
        self.options[name] = value

    async def set_prefix(self, value: str):
        await Prefix.update_or_create(dict(value=value), guild_id=self.guild_id)
        self.prefix = value

    async def add_banned_command(self, name: str):
        item: discord.ext.commands.Command = self.bot.get_command(name)
        if item is None:
            return Response("error", "The command does not exist.", 404)
        true_name = item.qualified_name
        if true_name in self.banned_commands:
            return Response(
                "success",
                "The command is already part of the banned commands list.",
                200,
            )
        else:
            command = DisabledCommand(guild_id=self.guild_id, name=true_name)
            await command.save()
            self.banned_commands.append(true_name)
            return Response("success", "The command has been added.", 200)

    async def add_restricted_command(self, name: str):
        item: discord.ext.commands.Command = self.bot.get_command(name)
        if item is None:
            return Response("error", "The command does not exist.", 404)
        true_name = item.qualified_name
        if true_name in self.restricted_commands:
            return Response(
                "success",
                "The command is already part of the restricted commands list.",
                200,
            )
        else:
            command = BotSpamCommand(guild_id=self.guild_id, name=true_name)
            await command.save()
            self.restricted_commands.append(true_name)
            return Response("success", "The command has been added.", 200)

    async def load_channels(self):
        async for item in NamedChannel.filter(guild_id=self.guild_id):
            self.channels[item.channel_name] = item.channel_id

    async def load_options(self):
        async for item in Option.filter(guild_id=self.guild_id):
            self.options[item.name] = item.enabled

    async def load_banned_commands(self):
        async for item in DisabledCommand.filter(guild_id=self.guild_id):
            self.banned_commands.append(item.name)

    async def load_restricted_commands(self):
        async for item in BotSpamCommand.filter(guild_id=self.guild_id):
            self.restricted_commands.append(item.name)

    async def load_prefix(self):
        item = await Prefix.filter(guild_id=self.guild_id).first()
        self.prefix = getattr(item, "value", "%")

    async def load_data(self):
        await asyncio.gather(
            self.load_channels(),
            self.load_options(),
            self.load_banned_commands(),
            self.load_restricted_commands(),
            self.load_prefix(),
            self.load_roles(),
        )

    async def remove_channel(self, name: str):
        channel = await NamedChannel.get_or_none(
            guild_id=self.guild_id, channel_name=name
        )
        if channel is not None:
            await channel.delete()
            self.channels.pop(name)
            return Response("success", "The channel mapping has been deleted.", 200)
        else:
            return Response("error", "The channel mapping does not exist.", 404)

    async def remove_banned_command(self, name: str):
        command = await DisabledCommand.get_or_none(guild_id=self.guild_id, name=name)
        if command is not None:
            await command.delete()
            return Response("success", "The command has been enabled.", 200)
        else:
            return Response("error", "The command is not disabled.", 404)

    async def remove_restricted_command(self, name: str):
        command = await BotSpamCommand.get_or_none(guild_id=self.guild_id, name=name)
        if command is not None:
            await command.delete()
            return Response("success", "The command can now be used anywhere.", 200)
        else:
            return Response("error", "The command is not restricted.", 404)

    def get_role(self, name: str, follow: bool = True) -> Optional[discord.Role]:
        if name not in self.roles:
            fallback = setup_constants["Roles"][name].fallback_role
            if fallback and follow:
                return self.get_role(fallback)
            else:
                return None
        else:
            return self.bot.get_guild(self.guild_id).get_role(self.roles[name])

    async def set_role(self, name: str, value: int):
        await NamedRole.update_or_create(
            role_name=name, guild_id=self.guild_id, defaults=dict(role_id=value)
        )
        self.roles[name] = value

    async def load_roles(self):
        async for item in NamedRole.filter(guild_id=self.guild_id):
            self.roles[item.role_name] = item.role_id
