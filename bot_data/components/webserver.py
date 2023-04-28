import logging
import sys
from typing import Iterable, Optional, Set, Tuple

import aiohttp.web

from . import Component
from .settings import Settings

logger = logging.getLogger(__name__)


class WebServer(Component):
    set_as = "web"

    require = [Settings]

    def __init__(self, bot):
        super().__init__(bot)
        self.app = aiohttp.web.Application()
        self.app["static_root_url"] = "/resources"
        self.runner = aiohttp.web.AppRunner(self.app)
        self.site: Optional[aiohttp.web.TCPSite] = None
        self.added: Set[Tuple[str, str, tuple]] = set()
        self.start_server = True  # Disabled by testing or other components

    async def init_async(self):
        pass

    @Component.event
    async def before_connection(self):
        await self.execute_event("before_webserver_load")
        await self.runner.setup()
        logger.debug("Starting webserver...")
        self.site = aiohttp.web.TCPSite(
            self.runner,
            self.bot.settings.bot_settings.webserver_ip,
            self.bot.settings.bot_settings.webserver_port,
        )
        if self.start_server:
            try:
                await self.site.start()
            except OSError as e:
                if e.errno == 48:
                    logger.info(
                        "The webserver cannot launch due to the port being already "
                        "taken. Exiting."
                    )
                    sys.exit(1)

    async def stop_async(self):
        logger.debug("Stopping webserver...")
        if self.site:
            try:
                await self.site.stop()
            except RuntimeError:
                pass

    def add_routes(self, routes: Iterable[aiohttp.web.RouteDef]) -> list:
        return [self.add_route(route) for route in routes]

    def add_route(self, route: aiohttp.web.RouteDef):
        route_hash = (route.method, route.path, tuple(route.kwargs.items()))
        if route_hash not in self.added:
            self.added.add(route_hash)
            return self.app.add_routes([route])[0]
