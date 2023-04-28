import logging
import os
import sys
from typing import Union

import aiohttp.web
import discord.ext.commands
import discord_slash.utils.manage_commands

from . import Component
from .sentry import Sentry
from .webserver import WebServer

actual_logger = logging.getLogger(__name__)


class Debug(Component):
    """Component that controls all debug actions. Please disable this comment on a PROD system."""

    require = [Sentry, WebServer]

    set_as = "debug"

    def __init__(self, bot):
        super().__init__(bot)
        self._on_command_error = self.bot.on_command_error
        self._on_error = self.bot.on_error
        self._on_slash_command_error = self.bot.on_slash_command_error
        self.debug = False
        self._create_option = discord_slash.utils.manage_commands.create_option
        self._span = None

    def do_debug_action(self):
        self.debug = True
        logger = logging.getLogger("bot_data")
        handler = logger.handlers[0]
        formatter = handler.formatter
        log_level = logger.level
        handler2 = logging.StreamHandler(sys.stdout)
        handler2.setFormatter(formatter)
        handler2.setLevel(log_level)
        logger.addHandler(handler2)
        logging.getLogger("backoff").addHandler(handler2)
        if os.getenv("LOG_ORM_SQL"):
            logging.getLogger("db_client").addHandler(handler2)
        # self.bot.web.app.add_routes(
        #     [
        #         aiohttp.web.static(
        #             "/resources",
        #             os.path.abspath(
        #                 os.path.join(__file__, "..", "..", "html", "resources")
        #             ),
        #         )
        #     ]
        # )
        self.bot.web.app.middlewares.append(self.show_400_stack_trace)
        self.bot.on_command_error = self.on_command_error
        self.bot.on_error = self.on_error
        self.bot.on_slash_command_error = self.on_slash_command_error
        discord_slash.utils.manage_commands.create_option = self.create_option

    def create_option(
        self,
        name: str,
        description: str,
        option_type: Union[int, type],
        required: bool,
        choices: list = None,
    ):
        if not (1 <= len(description) <= 100):
            raise ValueError("Description must be 1 <= len(description) <= 100.")
        return self._create_option(name, description, option_type, required, choices)

    async def init_async(self):
        self.do_debug_action()
        # Just comment out the above line to disable debug.
        pass

    async def stop_async(self):
        self.bot.on_command_error = self._on_command_error
        self.bot.on_error = self._on_error
        self.bot.on_slash_command_error = self._on_slash_command_error
        discord_slash.utils.manage_commands.create_option = self._create_option

    async def on_command_error(
        self, ctx: discord.ext.commands.Context, exc: BaseException
    ):
        actual_logger.exception(
            "Error on command %s: %s",
            ctx.command.qualified_name if ctx.command else ctx.invoked_with,
            str(exc),
            exc_info=exc,
        )
        await self._on_command_error(ctx, exc)

    async def on_error(self, event, *_, **__):
        actual_logger.exception("Error on event %s", event, exc_info=True)
        await self._on_error(event, *_, **__)

    async def on_slash_command_error(
        self, ctx: discord_slash.SlashContext, ex: BaseException
    ):
        actual_logger.exception("Error on slash command %s:", ctx.name, exc_info=ex)
        await self._on_slash_command_error(ctx, ex)

    @Component.event
    async def before_webserver_load(self):
        if self.debug:
            self.bot.web.app.middlewares.append(self.show_handler)

    @aiohttp.web.middleware
    async def show_400_stack_trace(self, request: aiohttp.web.Request, handler):
        try:
            return await handler(request)
        except aiohttp.web.HTTPBadRequest as e:
            actual_logger.debug(
                "Encountered HTTP 400 on %s %s",
                request.method,
                request.rel_url,
                exc_info=e,
            )
            raise

    @aiohttp.web.middleware
    async def show_handler(self, request: aiohttp.web.Request, handler):
        actual_logger.debug("Handler for %s is %r", request.url, handler)
        return await handler(request)
