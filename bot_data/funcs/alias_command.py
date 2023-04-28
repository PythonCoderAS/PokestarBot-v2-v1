import functools
import re
from typing import (
    Any,
    Callable,
    Coroutine,
    Optional,
    TYPE_CHECKING,
    Type,
    TypeVar,
    Union,
    Tuple,
    Mapping,
    List,
)

import discord.ext.commands
import discord_slash
from discord.ext.commands.core import hooked_wrapped_callback

from .general import _Sentinel, repr_template
from ..sentry.context import HubContext
from ..sentry.sentry import tags_from_values
from ..sentry.utils import start_transaction_or_child

if TYPE_CHECKING:
    from ..components.command_error import error_data_type

_ET = TypeVar("_ET", bound=discord.ext.commands.errors.CommandError)


class AliasCommand(discord.ext.commands.Command):
    symbols = re.compile(r"[_\-]")

    @property
    def callback(self):
        return super().callback

    @callback.setter
    def callback(self, function):
        discord.ext.commands.Command.callback.__set__(self, function)

        function = self._callback

        # Voodoo magic time:
        # Aself should normally be a context object, but cog commands will have that
        # "self" parameter. We cannot always assume that there will be a self
        # parameter either, so we need to assume both can be present and set "ctx" to
        # a Sentinel value, since None is a valid value to pass to a function.
        if not hasattr(function, "__pokestarbot_wrapped__"):

            @functools.wraps(function)
            async def wrapped(
                aself: Union[discord.ext.commands.Context, Any],
                ctx: Optional[discord.ext.commands.Context] = _Sentinel(),
                *args,
                **kwargs,
            ):
                actual_ctx = (
                    ctx
                    if isinstance(
                        ctx, (discord.ext.commands.Context, discord_slash.SlashContext)
                    )
                    else aself
                )
                if hasattr(actual_ctx, "hub"):
                    actual_ctx.hub.add_breadcrumb(
                        category="Command Log",
                        message=f"Running command {self.qualified_name}.",
                    )
                if isinstance(ctx, _Sentinel):
                    args = (aself, *args)
                else:
                    args = (aself, ctx, *args)
                if hasattr(actual_ctx, "hub"):
                    with start_transaction_or_child(
                        actual_ctx.hub,
                        name="Command " + self.qualified_name,
                        op="command",
                        description="Command " + self.qualified_name,
                    ) as span:
                        for name, value in tags_from_values(
                            actual_ctx.author,
                            actual_ctx.guild,
                            actual_ctx.channel,
                            self,
                        ).items():
                            span.set_tag(name, str(value))
                        return await function(*args, **kwargs)
                else:
                    return await function(*args, **kwargs)

            wrapped.__pokestarbot_wrapped__ = True
            self._callback = wrapped

    def apply_alias(self):
        uniques = set()
        aliases = set()
        for item in (self.name, *self.aliases):
            uniques.add(self.symbols.sub("(sep)", item))
        for item in uniques:
            aliases.add(item.replace("(sep)", ""))
            aliases.add(item.replace("(sep)", "-"))
            aliases.add(item.replace("(sep)", "_"))
        if self.name in aliases:
            aliases.remove(self.name)
        self.aliases = tuple(aliases)

    def __init__(self, *args, **kwargs) -> None:
        kwargs.setdefault("ignore_extra", True)
        super().__init__(*args, **kwargs)
        self.original_aliases = self.aliases
        self.apply_alias()
        self.exception_handlers: "error_data_type" = {}

    def exception_handler(self, exception: Type[_ET]):
        """Usage:

        @command.exception_handler(discord.ext.commmands.BadArgument)
        async def custom_error(ctx: HubContext, exc: discord.ext.commmands.BadArgument):
            return await ctx.send("...")
        """

        def do_decorate(
            func: Callable[
                [HubContext, _ET],
                Coroutine[Any, Any, Any],
            ]
        ) -> Callable[[HubContext, _ET], Coroutine[Any, Any, Any]]:
            self.exception_handlers[exception] = func
            return func

        return do_decorate

    async def special_invoke(self, ctx: discord.ext.commands.Context) -> None:
        # Overridden because we don't want the behavior of deleting invalid subcommands.
        await self.prepare(ctx)

        injected = hooked_wrapped_callback(self, ctx, self.callback)
        await injected(*ctx.args, **ctx.kwargs)

    def get_repr_args_and_kwargs(self) -> Tuple[List[str], Mapping[str, str]]:
        return ["name", "aliases", "cog"], {"full_name": "qualified_name"}

    def __repr__(self):
        args, kwargs = self.get_repr_args_and_kwargs()
        return repr_template(self, *args, **kwargs)


_original_invoke = discord.ext.commands.Command.invoke


async def invoke(self: discord.ext.commands.Command, ctx: discord.ext.commands.Context):
    if isinstance(self, AliasCommand):
        return await self.special_invoke(ctx)
    return await _original_invoke(self, ctx)


discord.ext.commands.Command.invoke = invoke
