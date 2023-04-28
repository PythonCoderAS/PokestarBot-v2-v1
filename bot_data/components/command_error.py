import logging
from typing import (
    Dict,
    Callable,
    Any,
    Coroutine,
    TypeVar,
    Type,
    Union,
    Protocol,
)

import discord.ext.commands.view
import discord_slash

from . import Component
from .orm import ORM
from ..funcs import (
    or_format,
    and_format,
    SendProtocol,
    InvalidCommand,
    SimpleLinkButtonView, ExtendedHelp,
)
from ..pager import Paginator
from ..sentry.context import HubContext

logger = logging.getLogger(__name__)

_ET = TypeVar("_ET", bound=discord.ext.commands.errors.CommandError)

error_data_type = Dict[
    Type[_ET],
    Callable[
        [HubContext, _ET],
        Coroutine[Any, Any, Any],
    ],
]


class ArgumentProto(Protocol):
    argument: str


class CommandError(Component):
    set_as = "command_error"

    require = [ORM]

    @staticmethod
    async def handle_missing_required_argument(
        ctx: HubContext, exc: discord.ext.commands.MissingRequiredArgument
    ):
        view = ExtendedHelp(ctx.bot.settings.bot_settings.base_domain, ctx.command)
        return await ctx.send(
            f"You are missing the `{exc.param.name}` argument.", view=view
        )

    @staticmethod
    async def ignore(ctx: HubContext, exc: _ET):
        pass

    @staticmethod
    async def handle_private_message_only(
        ctx: HubContext, _exc: discord.ext.commands.PrivateMessageOnly
    ):
        return await ctx.send("You can only use this command in a bot DM!")

    @staticmethod
    async def handle_guild_only(
        ctx: HubContext, _exc: discord.ext.commands.NoPrivateMessage
    ):
        return await ctx.send("You can only use this command in a server!")

    @staticmethod
    async def handle_not_owner(ctx: HubContext, _exc: discord.ext.commands.NotOwner):
        return await ctx.send("You are not the bot owner!")

    @staticmethod
    def handle_not_found(noun: str):
        async def do_handle(ctx: HubContext, exc: ArgumentProto):
            return await ctx.send(f"The {noun} `{exc.argument}` was not found.")

        return do_handle

    @staticmethod
    def handle_invalid(noun: str):
        async def do_handle(ctx: HubContext, exc: ArgumentProto):
            return await ctx.send(
                f"The argument `{exc.argument}` is an invalid {noun}."
            )

        return do_handle

    @staticmethod
    async def handle_bad_literal(
        ctx: HubContext, exc: discord.ext.commands.BadLiteralArgument
    ):
        ctx.view.undo()
        argument = ctx.view.get_quoted_word()
        embed = discord.Embed(title=f"Valid Values for Argument {exc.param.name}")
        paginator = Paginator.from_lines(embed, [f"`{item}`" for item in exc.literals])
        paginator.add_text_to_all_pages(
            f"The argument `{argument}` is not part of the list of valid values."
        )
        return await paginator.send(ctx)

    @staticmethod
    async def handle_disabled_command(
        ctx: HubContext, _exc: discord.ext.commands.DisabledCommand
    ):
        return await ctx.send(
            f"`{ctx.clean_prefix}{ctx.command.qualified_name}` is disabled!"
        )

    @staticmethod
    async def handle_command_cooldown(
        ctx: HubContext, exc: discord.ext.commands.CommandOnCooldown
    ):
        return await ctx.send(
            f"The command `{ctx.clean_prefix}{ctx.command.qualified_name}` is on "
            f"cooldown! You can try again in {exc.retry_after:2f} seconds."
        )

    max_concurrency_data: Dict[Union[discord.ext.commands.BucketType, int], str] = {
        discord.ext.commands.BucketType.default: (
            "The command `{ctx.clean_prefix}{ctx.command.qualified_name}` can only be "
            "ran concurrently {amount_format} in all servers and DMs!"
        ),
        discord.ext.commands.BucketType.user: (
            "The command `{ctx.clean_prefix}{ctx.command.qualified_name}` can only be "
            "ran concurrently by you {amount_format} in all servers and DMs!"
        ),
        discord.ext.commands.BucketType.guild: (
            "The command `{ctx.clean_prefix}{ctx.command.qualified_name}` can only be "
            "ran concurrently in this server {amount_format}!"
        ),
        discord.ext.commands.BucketType.channel: (
            "The command `{ctx.clean_prefix}{ctx.command.qualified_name}` can only be "
            "ran concurrently in this channel {amount_format}!"
        ),
        discord.ext.commands.BucketType.member: (
            "The command `{ctx.clean_prefix}{ctx.command.qualified_name}` can only be "
            "ran concurrently by you {amount_format} in this guild!"
        ),
        discord.ext.commands.BucketType.category: (
            "The command `{ctx.clean_prefix}{ctx.command.qualified_name}` can only be "
            "ran concurrently in this channel category {amount_format}!"
        ),
        discord.ext.commands.BucketType.role: (
            "The command `{ctx.clean_prefix}{ctx.command.qualified_name}` can only be "
            "ran concurrently by the {ctx.author.top_role.mention} role {amount_format}!"
        ),
        -1: (
            "The command `{ctx.clean_prefix}{ctx.command.qualified_name}` can only be "
            "ran concurrently {amount_format}."
        ),
    }

    @classmethod
    async def handle_max_concurrency(
        cls, ctx: HubContext, exc: discord.ext.commands.MaxConcurrencyReached
    ):
        amount_format = str(exc.number) + " " + "time" if exc.number == 1 else "times"
        return await ctx.send(
            cls.max_concurrency_data.get(exc.per, -1).format(
                amount_format=amount_format, ctx=ctx
            ),
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @staticmethod
    def get_role_object(role_item: Union[str, int], guild: discord.Guild):
        if isinstance(role_item, int):
            role = discord.utils.get(guild.roles, id=role_item)
        else:
            role = discord.utils.get(guild.roles, name=role_item)
        return role.mention if role else "**Invalid Role**"

    @classmethod
    def handle_missing_role(cls, noun: str):
        async def do_handle(
            ctx: HubContext,
            exc: Union[
                discord.ext.commands.MissingRole,
                discord.ext.commands.MissingAnyRole,
                discord.ext.commands.BotMissingRole,
                discord.ext.commands.BotMissingAnyRole,
            ],
        ):
            if isinstance(
                exc,
                (discord.ext.commands.MissingRole, discord.ext.commands.BotMissingRole),
            ):
                missing_role = exc.missing_role
                role_mention = cls.get_role_object(missing_role, ctx.guild)
                return await ctx.send(
                    f"{noun.title()} are missing the {role_mention} role!",
                    allowed_mentions=discord.AllowedMentions.none(),
                )
            else:
                role_mentions = [
                    cls.get_role_object(missing_role, ctx.guild)
                    for missing_role in exc.missing_roles
                ]
                return await ctx.send(
                    f"{noun.title()} are missing the "
                    f"{or_format(role_mentions)} roles!",
                    allowed_mentions=discord.AllowedMentions.none(),
                )

        return do_handle

    @staticmethod
    async def handle_missing_nsfw(
        ctx: HubContext, _exc: discord.ext.commands.NSFWChannelRequired
    ):
        return await ctx.send(
            f"The command `{ctx.clean_prefix}{ctx.command.qualified_name}` "
            f"can only be run in an NSFW channel!"
        )

    @staticmethod
    def handle_missing_permissions(noun: str):
        async def do_handle(
            ctx: HubContext,
            exc: Union[
                discord.ext.commands.MissingPermissions,
                discord.ext.commands.BotMissingPermissions,
            ],
        ):
            perms_formatted = [
                perm.replace("_", " ").replace("guild", "server").title()
                for perm in exc.missing_permissions
            ]
            if len(perms_formatted) == 1:
                return await ctx.send(
                    f"{noun.title()} are missing the "
                    f"{perms_formatted[0]} permission!"
                )
            return await ctx.send(
                f"{noun.title()} are missing the "
                f"{and_format(perms_formatted)} permissions!"
            )

        return do_handle

    @staticmethod
    async def handle_unexpected_quote_mark(
        ctx: HubContext, _exc: discord.ext.commands.UnexpectedQuoteError
    ):
        view = ctx.view
        view.undo()
        item: str = view.get_word()
        escaped = item
        for quote in discord.ext.commands.view._all_quotes:
            escaped = escaped.replace(quote, "\\" + quote)
        return await ctx.send(
            f"Invalid quote in argument `{item}`. If you really want to use"
            f" the quote, please escape the quote, such as `{escaped}`."
        )

    def __init__(self, bot):
        super().__init__(bot)
        self.error_data: error_data_type = {
            discord.ext.commands.MissingRequiredArgument: (
                self.handle_missing_required_argument
            ),
            discord.ext.commands.CommandNotFound: self.ignore,
            discord.ext.commands.ConversionError: self.fallback_error,
            discord.ext.commands.CommandInvokeError: self.fallback_error,
            discord.ext.commands.ExtensionFailed: self.fallback_error,
            discord.ext.commands.MemberNotFound: self.handle_not_found("member"),
            discord.ext.commands.RoleNotFound: self.handle_not_found("role"),
            discord.ext.commands.UserNotFound: self.handle_not_found("user"),
            discord.ext.commands.ChannelNotFound: self.handle_not_found("channel"),
            discord.ext.commands.EmojiNotFound: self.handle_not_found("emoji"),
            discord.ext.commands.GuildNotFound: self.handle_not_found("guild"),
            discord.ext.commands.MessageNotFound: self.handle_not_found("message"),
            discord.ext.commands.BadBoolArgument: self.handle_invalid("boolean"),
            discord.ext.commands.BadColourArgument: self.handle_invalid("color"),
            discord.ext.commands.BadFlagArgument: self.handle_invalid("flag"),
            discord.ext.commands.BadInviteArgument: self.handle_invalid("invite"),
            discord.ext.commands.BadLiteralArgument: self.handle_bad_literal,
            discord.ext.commands.PartialEmojiConversionFailure: self.handle_invalid(
                "emoji"
            ),
            InvalidCommand: self.handle_not_found("command"),
            discord.ext.commands.DisabledCommand: self.handle_disabled_command,
            discord.ext.commands.CommandOnCooldown: self.handle_command_cooldown,
            discord.ext.commands.MaxConcurrencyReached: self.handle_max_concurrency,
            discord.ext.commands.MissingRole: self.handle_missing_role("you"),
            discord.ext.commands.MissingAnyRole: self.handle_missing_role("you"),
            discord.ext.commands.BotMissingRole: self.handle_missing_role("bot"),
            discord.ext.commands.BotMissingAnyRole: self.handle_missing_role("bot"),
            discord.ext.commands.NSFWChannelRequired: self.handle_missing_nsfw,
            discord.ext.commands.MissingPermissions: self.handle_missing_permissions(
                "you"
            ),
            discord.ext.commands.BotMissingPermissions: self.handle_missing_permissions(
                "bot"
            ),
            discord.ext.commands.UnexpectedQuoteError: self.handle_unexpected_quote_mark,
        }
        self._on_command_error = None

    async def fallback_error(
        self, ctx: Union[HubContext, discord_slash.SlashContext], exc: BaseException
    ):
        return await self._on_command_error(ctx, exc)

    async def init_async(self):
        pass

    async def stop_async(self):
        if self._on_command_error is not None:
            self.bot.on_command_error = self._on_command_error

    @Component.event()
    async def before_connection(self):
        self._on_command_error = self.bot.on_command_error
        self.bot.on_command_error = self.on_command_error

    @staticmethod
    async def resolve_error_data(
        ctx: HubContext,
        exc: discord.ext.commands.CommandError,
        error_data: error_data_type,
    ):
        exc_type = type(exc)
        if exc_type in error_data:
            try:
                await error_data[exc_type](ctx, exc)
            except discord.ext.commands.CommandError as e:
                return e
            return True
        for given_type in error_data.keys():
            if isinstance(exc, given_type):
                await error_data[given_type](ctx, exc)
                return True
        return False

    async def send_error_message(self, send_method: SendProtocol, error_id: str):
        owner = self.bot.get_user(self.bot.owner_id)
        owner_name = owner.name + "#" + owner.discriminator
        return await send_method(
            f"Oh no! The bot has encountered an error! {owner.mention} has been "
            f"notified. If you would like to know more about the error, please "
            f"contact `{owner_name}` with ID `{error_id}`."
        )

    async def on_command_error(
        self, ctx: HubContext, exc: discord.ext.commands.CommandError
    ):
        command_specific_handler = await self.resolve_error_data(ctx, exc, ctx.exception_handlers)
        if not isinstance(command_specific_handler, bool):
            # returns boolean or an exception
            if command_specific_handler != exc:
                # a handler raised a different exception, time to restart the chain!
                return await self.on_command_error(ctx, command_specific_handler)
            else:
                command_specific_handler = False
                # Reraising the same exception is similar to a False.
        if not command_specific_handler:
            global_handler = await self.resolve_error_data(ctx, exc, self.error_data)
            if not isinstance(global_handler, bool):
                if global_handler != exc:
                    # a handler raised a different exception, time to restart the chain!
                    return await self.on_command_error(ctx, global_handler)
                else:
                    global_handler = False
                    # Reraising the same exception is similar to a False.
            if not global_handler:
                return await self.fallback_error(ctx, exc)
            else:
                logger.debug("Global error handler dealt with error %s",
                             exc)
        else:
            logger.debug("Command %s's error-specific handler dealt with error %s",
            ctx.command.qualified_name,
                         exc)
