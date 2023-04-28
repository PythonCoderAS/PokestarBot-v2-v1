import asyncio
import functools
import inspect
import logging
import sys
import types
import uuid
from typing import List, Type, TypeVar, Any, Callable

import discord.ext.commands
import discord_slash
import sentry_sdk
import tortoise.backends.asyncpg

from . import Component
from ..funcs import start_transaction_or_child
from ..sentry.context import HubContext
from ..sentry.hub import CustomHub
from ..sentry.sentry import (
    report_exception,
    tags_from_context,
    context_from_user,
    context_from_channel,
    context_from_guild,
    tags_from_values,
)

logger = logging.getLogger(__name__)

ContextType = TypeVar("ContextType", bound=discord.ext.commands.Context)


class Sentry(Component):
    """Handles Sentry integration."""

    set_as = "sentry"

    def __init__(self, bot):
        super().__init__(bot)
        self._get_context = self.bot.get_context
        self._on_command_error = self.bot.on_command_error
        self._on_error = self.bot.on_error
        self.hubs: List[sentry_sdk.Hub] = []
        self._on_slash_command_error = self.bot.slash_client.on_slash_command_error
        self._dispatch = self.bot.dispatcher
        self._execute_query = tortoise.backends.asyncpg.AsyncpgDBClient.execute_query
        self._execute_query_dict = (
            tortoise.backends.asyncpg.AsyncpgDBClient.execute_query_dict
        )
        self._execute_many = tortoise.backends.asyncpg.AsyncpgDBClient.execute_many
        self._execute_insert = tortoise.backends.asyncpg.AsyncpgDBClient.execute_insert
        self._execute_script = tortoise.backends.asyncpg.AsyncpgDBClient.execute_script
        self._invoke_command = self.bot.slash_client.invoke_command
        self._original_http_methods = {
            name: getattr(self.bot.http, name) for name in self.get_methods_to_replace()
        }
        self._sleep = asyncio.sleep

    async def init_async(self):
        self.bot.get_context = self.get_context
        self.bot.on_command_error = self.on_command_error
        self.bot.on_error = self.on_error
        self.bot.on_slash_command_error = self.on_slash_command_error
        self.bot.dispatcher = self.dispatch
        self.bot.slash_client.invoke_command = self.invoke_command
        asyncio.sleep = self.sleep

    async def stop_async(self):
        self.bot.get_context = self._get_context
        self.bot.on_command_error = self._on_command_error
        self.bot.on_error = self._on_error
        self.bot.on_slash_command_error = self._on_slash_command_error
        self.bot.dispatcher = self._dispatch
        self.bot.slash_client.invoke_command = self._invoke_command
        asyncio.sleep = self._sleep
        self.restore_tortoise_orm()
        self.revert_discord_http_session_request_patch()
        self.revert_discord_http_patch()
        # [hub.client.close() for hub in self.hubs]

    @Component.event
    async def on_init_complete(self):
        self.__session = getattr(self.bot.http, "_HTTPClient__session", None)
        if self.__session is None:
            logger.warning("self.bot.http._HTTPClient__session is None!")
        self._discord_http_session_request = self.__session._request
        self.apply_discord_http_patch()
        self.apply_discord_http_session_request_patch()
        self.generate_tortoise_orm_wrappers()

    async def get_context(
        self, message: discord.Message, *, cls: Type[ContextType] = HubContext
    ) -> ContextType:
        return await self._get_context(message, cls=cls)

    def dispatch(self, event_name, *args, **kwargs):
        if event_name in ["connect", "ready", "guild_join"]:
            with start_transaction_or_child(
                op="event",
                name="Event Dispatch" + event_name,
                description="Event Dispatch",
            ) as span:
                span.set_tag("event", event_name)
                return self._dispatch(event_name, *args, **kwargs)
        else:
            return self._dispatch(event_name, *args, **kwargs)

    async def on_command_error(self, context: HubContext, exception: BaseException):
        error_id = exception.__pokestarbot_error_id__ = str(uuid.uuid4())
        await self.bot.command_error.send_error_message(context.send, error_id)
        report_exception(
            exception, context, tag_data=tags_from_context(context), error_id=error_id
        )

    async def on_error(self, event: str, *_, **__):
        report_exception(sys.exc_info()[1], tag_data={"event": event})

    async def on_slash_command_error(
        self, ctx: discord_slash.SlashContext, ex: BaseException
    ):
        sentry_context = {
            **context_from_user(
                ctx.author,
                ctx.channel
                if isinstance(ctx.channel, discord.abc.GuildChannel)
                else None,
            ),
            **context_from_guild(ctx.guild),
            **context_from_channel(ctx.channel, ctx.bot.user),
        }
        report_exception(
            ex,
            context=sentry_context,
            hub=ctx.hub,
            tag_data=tags_from_values(ctx.author, ctx.guild, ctx.channel, None),
        )

    def get_hub(self):
        frame: types.FrameType = sys._getframe(1)
        hub = None
        while frame.f_back:
            for item in frame.f_locals.values():
                if (
                    isinstance(item, HubContext)
                    or isinstance(item, discord_slash.SlashContext)
                    and hasattr(item, "hub")
                ):
                    hub = item.hub
                    if not hub.scope.span:
                        continue
                elif isinstance(item, sentry_sdk.Hub):
                    hub = item
                    if not hub.scope.span:
                        continue
                if hub:
                    if hub == sentry_sdk.Hub.main:
                        continue
                    return hub
            frame = frame.f_back
        return None

    def wrap_db_method(self, func: Callable[..., Any], name: str) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            hub = self.get_hub()
            if hub is None:
                return func(*args, **kwargs)
            actual_name = name + ": " + args[1]
            with start_transaction_or_child(
                hub, name=actual_name, op="db", description=actual_name
            ):
                return func(*args, **kwargs)

        return wrapped

    def generate_tortoise_orm_wrappers(self):
        tortoise.backends.asyncpg.AsyncpgDBClient.execute_query = self.wrap_db_method(
            self._execute_query, "Execute Query"
        )
        tortoise.backends.asyncpg.AsyncpgDBClient.execute_query_dict = (
            self.wrap_db_method(self._execute_query_dict, "Execute Query Dict")
        )
        tortoise.backends.asyncpg.AsyncpgDBClient.execute_many = self.wrap_db_method(
            self._execute_many, "Execute Many"
        )
        tortoise.backends.asyncpg.AsyncpgDBClient.execute_insert = self.wrap_db_method(
            self._execute_insert, "Execute Insert"
        )
        tortoise.backends.asyncpg.AsyncpgDBClient.execute_script = self.wrap_db_method(
            self._execute_script, "Execute Script"
        )

    def restore_tortoise_orm(self):
        tortoise.backends.asyncpg.AsyncpgDBClient.execute_query = self._execute_query
        tortoise.backends.asyncpg.AsyncpgDBClient.execute_query_dict = (
            self._execute_query_dict
        )
        tortoise.backends.asyncpg.AsyncpgDBClient.execute_many = self._execute_many
        tortoise.backends.asyncpg.AsyncpgDBClient.execute_insert = self._execute_insert
        tortoise.backends.asyncpg.AsyncpgDBClient.execute_script = self._execute_script

    @staticmethod
    def qualified_name(ctx: discord_slash.SlashContext):
        parts = [ctx.name, ctx.subcommand_group, ctx.subcommand_name]
        while None in parts:
            parts.remove(None)
        return " ".join(parts)

    async def invoke_command(
        self,
        func: discord_slash.SlashCommand,
        ctx: discord_slash.SlashContext,
        *args,
        **kwargs
    ):
        ctx.hub = CustomHub(sentry_sdk.Hub.current)
        name = "Slash Command /" + self.qualified_name(ctx)
        with start_transaction_or_child(
            ctx.hub, name=name, op="slash_command", description=name
        ) as span:
            for name, value in tags_from_values(
                ctx.author, ctx.guild, ctx.channel, None
            ).items():
                span.set_tag(name, str(value))
            span.set_tag("slash_command_name", name)
            return await self._invoke_command(func, ctx, *args, **kwargs)

    def get_methods_to_replace(self):
        names = []
        http = self.bot.http
        for item in dir(http):
            if not item.startswith("_"):
                val = getattr(http, item)
                if callable(val):
                    source = inspect.getsource(val)
                    if "return self.request(" in source:
                        names.append(item)
        return names

    def patch_discord_http(self, name: str):
        func: types.FunctionType = getattr(self.bot.http, name)
        clean_name = name.replace("_", " ").title()
        sig = inspect.signature(func)

        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            hub = self.get_hub()
            if hub is None:
                return await func(*args, **kwargs)
            with start_transaction_or_child(
                hub, name=clean_name, op="discord_http", description=clean_name
            ) as span:
                resolved = sig.bind(*args, **kwargs)
                resolved.apply_defaults()
                for key, val in resolved.arguments.items():
                    span.set_tag(key, str(val))
                return await func(*args, **kwargs)

        setattr(self.bot.http, name, wrapped)

    def apply_discord_http_patch(self):
        for name in self._original_http_methods.keys():
            self.patch_discord_http(name)

    def revert_discord_http_patch(self):
        for name, orig in self._original_http_methods.items():
            setattr(self.bot.http, name, orig)

    def apply_discord_http_session_request_patch(self):

        self.__session._request = functools.partial(
            self.bot.session.request_inner, self.__session._request
        )

    def revert_discord_http_session_request_patch(self):
        if hasattr(self, "_discord_http_session_request"):
            self.__session._request = self._discord_http_session_request

    async def sleep(self, amount: float, *args, **kwargs):
        hub = self.get_hub()
        if hub is None:
            return await self._sleep(amount, *args, **kwargs)
        with start_transaction_or_child(
            hub, name="Sleep", op="sleep", description="Sleep"
        ) as span:
            span.set_tag("Time", str(amount))
            return await self._sleep(amount, *args, **kwargs)
