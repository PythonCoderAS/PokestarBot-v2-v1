"""
This file houses the PokestarBot class, which is the main entryway to my bot.
"""
import importlib
import logging
import os
import sys
import unittest.mock
from typing import Coroutine, Dict, List, NoReturn, Type, Any

import discord.ext.commands
import uvloop

from bot_data import stop_discord_slash_dpy_overrides
from bot_data.components import Component
from bot_data.components.command_error import CommandError
from bot_data.components.console import Console
from bot_data.components.debug import Debug
from bot_data.components.http import Session
from bot_data.components.menu import MenuComponent
from bot_data.components.sentry import Sentry
from bot_data.components.settings import Settings
from bot_data.components.stats import Stat
from bot_data.components.timezone import Timezone
from bot_data.components.webserver import WebServer
from bot_data.creds import TOKEN as bot_token
from bot_data.log import setup_logging

logger = logging.getLogger(__name__)


class PokestarBot(discord.ext.commands.Bot):
    """My bot."""

    def __init__(self, **kwargs):
        """Initializes the bot by setting the intents."""
        intents = discord.Intents.all()
        for key, value in {
            "activity": discord.Game("%help • %support"),
            "case_insensitive": True,
            "strip_after_prefix": True,
            "intents": intents,
        }.items():
            kwargs.setdefault(key, value)
        super().__init__(
            "%",
            # This is a temporary measure, the actual method will get loaded in soon.
            **kwargs
        )
        self.components: Dict[str, Component] = {}
        self.component_instance_ordered: List[Component] = []
        # self.slash_client = discord_slash.SlashCommand(
        #     self, sync_commands=True, sync_on_cog_reload=True,
        #     delete_from_unused_guilds=True
        # )
        self.slash_client = unittest.mock.MagicMock()
        stop_discord_slash_dpy_overrides()
        self.console: Console
        self.stat: Stat
        self.settings: Settings
        self.menu: MenuComponent
        self.session: Session
        self.web: WebServer
        self.tz: Timezone
        self.sentry: Sentry
        self.debug: Debug
        self.command_error: CommandError
        self.kwargs_used_on_init = kwargs
        self.started = False
        self.dispatcher = super().dispatch

    async def close(self):
        logger.info("Closing bot")
        [
            await self.run_coro_exception_free(item.stop_async())
            for item in reversed(self.component_instance_ordered)
        ]
        logger.debug("Finished custom behavior, running final shutdown...")
        if self.started:
            return await super().close()

    @staticmethod
    async def run_coro_exception_free(coro: Coroutine):
        try:
            return await coro
        except Exception as e:
            logger.exception("Encountered error while running coroutine: ", exc_info=e)

    async def init_async(self):
        """Initializes the async parts of the bot."""
        # Note: This must come first so that the ORM is loaded for components that need it.
        await self.load_components()

    def start_bot_without_run(self):
        self.loop.run_until_complete(self.init_async())
        try:
            self.load_extensions()
        except Exception as e:
            logger.critical("Error while loading extensions: ", exc_info=e)
            self.loop.run_until_complete(self.close())
            sys.exit(1)

    def start_bot(self) -> NoReturn:
        """Starts the bot."""
        self.start_bot_without_run()
        self.run(bot_token)

    async def on_ready(self):
        logger.debug("Bot ready.")

    def load_component_class(self, name: str):
        name = name.lower()
        mod = importlib.import_module("bot_data.components." + name)
        if not hasattr(mod, "component_class"):
            for val in vars(mod).copy().values():
                if (
                    isinstance(val, type)
                    and issubclass(val, Component)
                    and val != Component
                ):
                    mod.component_class = val
        elif getattr(mod, "component_class", -1) is None:
            return
        return mod.component_class

    async def load_component_instance(self, name: str, c_class: Type[Component]):
        inst: Component = c_class(self)
        self.components[name] = inst
        if c_class.set_as:
            setattr(self, c_class.set_as, inst)
        try:
            await inst.init_async()
        except Exception as e:
            logger.critical("Critical exception. Shutting down bot.", exc_info=e)
            await self.close()
            sys.exit(1)
        return inst

    async def load_components(self):
        components = {}
        component_backlog = {}
        base = os.path.abspath(os.path.join(__file__, "..", "components"))
        for file in os.listdir(base):
            if file.endswith(".py") or (
                os.path.isdir(os.path.join(base, file))
                and os.path.exists(os.path.join(base, file, "__init__.py"))
            ):
                name = os.path.splitext(file)[0]
                c_class = self.load_component_class(name)
                if not c_class:
                    continue
                if c_class.require:
                    component_backlog[name] = c_class
                else:
                    components[name] = c_class
        while component_backlog:
            for name, item in component_backlog.copy().items():
                if set(components.values()).issuperset(set(item.require)):
                    components[name] = item
                    component_backlog.pop(name)
        self.component_instance_ordered = [
            await self.load_component_instance(name, c_type)
            for name, c_type in components.items()
        ]

    def load_extensions(self):
        self.load_extension("bot_data.extensions.cogs")  # Needs to go first!
        root_dir = os.path.abspath(os.path.join(__file__, "..", "extensions"))
        for file in os.listdir(root_dir):
            if (
                not file.startswith("_")
                and (
                    os.path.isdir(os.path.join(root_dir, file)) or file.endswith(".py")
                )
                and file != "cogs.py"
            ):
                if "." in file:
                    name, sep, ext = file.rpartition(".")
                else:
                    name = file
                try:
                    self.load_extension("bot_data.extensions.{}".format(name))
                except discord.ext.commands.ExtensionAlreadyLoaded:
                    pass

    def dispatch(self, *args, **kwargs):
        return self.dispatcher(*args, **kwargs)

    def run(self, *args: Any, **kwargs: Any):
        self.started = True
        super().run(*args, **kwargs)


def main() -> NoReturn:
    """
    The main function that does the initial setup of the bot.

    In order, the setup function:

    #. Initializes the logging system with :func:setup_logging
    #. Installs a :class:`uvloop.EventLoopPolicy`.
    #. Initializes a :class:`PokestarBot`.
    #. Runs it.
    """
    logging_data = setup_logging("bot_data")
    uvloop.install()
    bot = PokestarBot()
    bot._logging_data = logging_data
    bot.start_bot()
