import abc
import asyncio
import dataclasses
import enum
import inspect
import itertools
from typing import (
    Callable,
    List,
    TYPE_CHECKING,
    Type,
    TypeVar,
    Union,
    Protocol,
    Literal,
)

import discord.ext.commands
import discord_slash
from discord.ext.commands import Context
from discord.ext.commands.converter import T_co

from .alias_command import AliasCommand
from .discord_views import *  # noqa
from .general import run_coro_sync
from ..exceptions import InvalidEnumConversion
from ..sentry.context import HubContext
from ..sentry.sentry import tags_from_values
from ..sentry.utils import start_transaction_or_child
from ..setup import setup_constants

if TYPE_CHECKING:
    pass

_EnumT = TypeVar("_EnumT", bound=enum.Enum, covariant=True)


def get_overwrite(name: str) -> discord.PermissionOverwrite:
    return setup_constants["Roles"][name].permission_overwrite


async def apply_all_overwrites(
    guild: discord.Guild,
    role: discord.Role,
    overwrite: discord.PermissionOverwrite,
) -> bool:
    if not (
        guild.me.guild_permissions.administrator
        or guild.me.guild_permissions.manage_channels
    ):
        return True
    for channel in guild.channels:
        overwrites = channel.overwrites
        if role not in overwrites or overwrites[role] != overwrite:
            overwrites[role] = overwrite
            await channel.edit(
                overwrites=overwrites,
                reason=f"Adding override for {role.name} role due to command trigger.",
            )
    return False


async def delete_messages_or_ignore(
    channel: discord.abc.Messageable, *messages, has_permissions: bool = False
):
    if not messages:
        return
    if isinstance(channel, discord.TextChannel) and has_permissions:
        try:
            await channel.delete_messages(*messages)
        except Exception:
            pass
    else:
        try:
            await messages[0].delete()
        except Exception:
            pass


async def has_prefix(bot: discord.ext.commands.Bot, message: discord.Message):
    if message.content:
        entry = await bot.get_prefix(message)
        return message.content.startswith(
            tuple(entry) if not isinstance(entry, str) else entry
        )
    return False


async def get_response(
    bot: discord.ext.commands.Bot,
    channel: Optional[Union[discord.TextChannel, discord.DMChannel]],
    message: Optional[Union[str, discord.Message]] = None,
    check: Callable[[discord.Message], bool] = lambda msg: True,
    on_timeout: Optional[Callable[[], Coroutine[Any, Any, Any]]] = None,
    delete: bool = False,
) -> Optional[discord.Message]:
    if isinstance(message, str):
        if isinstance(channel, discord.Webhook):
            msg = await channel.send(message, wait=True)
        else:
            msg = await channel.send(message)
    else:
        msg = message
    if any((msg is None, channel is None)):
        to_delete = []
        can_delete_other_messages = False
    else:
        to_delete = [msg]
        guild = getattr(channel, "guild", None)
        me = guild.me if guild is not None else bot.user
        can_delete_other_messages = channel.permissions_for(me).manage_messages
    try:
        with start_transaction_or_child(
            bot.sentry.get_hub(),
            op="listen",
            name="Listen for Message",
            description="Listen for Message",
        ) as span:
            for name, value in tags_from_values(
                message.author if message else None,
                message.guild if message else None,
                channel if channel else None,
                None,
            ).items():
                span.set_tag(name, str(value))
        resp: discord.Message = await bot.wait_for(
            "message",
            check=lambda message: (
                message.channel.id == channel.id if channel else True
            )
            and not run_coro_sync(has_prefix(bot, message))
            and check(message),
            timeout=60,
        )
    except asyncio.TimeoutError:
        if on_timeout:
            await on_timeout()
        return None
    else:
        if can_delete_other_messages:
            to_delete.append(resp)
        return resp
    finally:
        if delete:
            asyncio.create_task(
                delete_messages_or_ignore(
                    channel, *to_delete, has_permissions=can_delete_other_messages
                )
            )


async def try_conversion(
    converter: Union[
        Type[discord.ext.commands.Converter], discord.ext.commands.Converter
    ],
    argument: str,
    context: discord.ext.commands.Context,
) -> Optional[Any]:
    if isinstance(converter, type):
        converter = converter()
    try:
        return await converter.convert(context, argument)
    except discord.ext.commands.BadArgument:
        return None


def in_guilds(guild_ids: Optional[List[int]]):
    async def predicate(ctx: HubContext):
        if guild_ids is None:
            return True
        return bool(ctx.guild_id in guild_ids)

    return discord.ext.commands.check(predicate)


async def generate_subcommand_pager(
    ctx: HubContext,
    group: discord.ext.commands.Group,
    embed: Optional[discord.Embed] = None,
    title: Optional[str] = None,
):
    from ..pager import Paginator

    if (embed, title).count(None) != 1:
        raise ValueError("Either embed or title must be specified.")
    l = []
    for item in sorted(group.commands, key=lambda command: command.name):
        l.append(f"`{ctx.prefix}{group.qualified_name} {item.name}`")
    if not embed:
        online_help_url = ctx.bot.settings.get_absolute_url_from_relative(
            "/help/commands/" + group.qualified_name.replace(" ", "/")
        )
        embed = discord.Embed(
            title=title or f"{ctx.prefix}{group.qualified_name} Subcommands"
        )
        embed.add_field(
            name="Detailed Help",
            value=f"View help online at {online_help_url}.",
            inline=False,
        )
    pager = Paginator.from_lines(embed, l)
    return await pager.send(ctx)


class EmbedFixed(discord.Embed):
    """Embed with __bool__"""

    def __bool__(self):
        d: dict = self.to_dict()
        d.pop("type")
        return bool(d)


def raise_missing_arg(name: str):
    raise discord.ext.commands.MissingRequiredArgument(
        inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    )


async def trigger_respective_command_error(
    ctx: Union[discord_slash.SlashContext, HubContext], exc: BaseException
):
    if isinstance(ctx, discord.ext.commands.Context):
        return await ctx.bot.on_command_error(ctx, exc)
    return await ctx.bot.slash_client.on_slash_command_error(ctx, exc)


@dataclasses.dataclass(repr=False)
class FlagTemplate(
    discord.ext.commands.FlagConverter,
    prefix="--",
    delimiter="=",
    case_insensitive=True,
):
    def __post_init__(self):
        for name, item in self.get_flags().items():
            setattr(self, name, item.default)


class EnumConverter(
    discord.ext.commands.Converter[_EnumT],
    abc.ABC,
):
    def __init__(self, enum: Type[_EnumT]):
        self.enum = enum

    async def convert(
        self, _ctx: Optional[discord.ext.commands.Context], argument: str
    ) -> _EnumT:
        try:
            return getattr(self.enum, argument)
        except ValueError:
            try:
                return self.enum(int(argument))
            except ValueError as exc:
                raise InvalidEnumConversion(self.enum.__name__, argument) from exc


def generate_literal_from_enum(enum: Type[_EnumT]):
    return Literal[
        tuple(itertools.chain(*((str(item.name), str(item.value)) for item in enum)))
    ]


class SendProtocol(Protocol):
    async def __call__(
        self,
        content: Optional[str] = None,
        *,
        embed: Optional[discord.Embed] = None,
        **kwargs: Any,
    ):
        ...


class InvalidCommand(discord.ext.commands.BadArgument):
    def __init__(self, command: str, *args):
        super().__init__(*args)
        self.command = self.argument = command


class CommandConverter(discord.ext.commands.Converter[AliasCommand]):
    async def convert(
        self, ctx: discord.ext.commands.Context, argument: str
    ) -> AliasCommand:
        val = ctx.bot.get_command(argument)
        if val is None:
            raise InvalidCommand(argument)
        else:
            return val
