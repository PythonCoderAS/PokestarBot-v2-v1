from . import Component
from .webserver import WebServer


class BotTesting(Component):
    require = [WebServer]

    @property
    def testing(self):
        return self.bot.kwargs_used_on_init.get("is_testing", False)

    async def init_async(self):
        if self.testing:
            self.bot.web.start_server = False
