from . import Component


class ExtendedComponentFunctionality(Component):
    """Controls additional Component methods."""

    def __init__(self, bot):
        super().__init__(bot)
        self._old_login = self.bot.login
        self._old_on_ready = getattr(self.bot, "on_ready", None)
        self._on_ready_ran_once = False

    async def init_async(self):
        self.bot.login = self.login
        self.bot.on_ready = self.on_ready

    async def stop_async(self):
        self.bot.login = self._old_login
        if self._old_on_ready:
            self.bot.on_ready = self._old_on_ready
        else:
            del self.bot.on_ready

    async def login(self, *args, **kwargs):
        await self.execute_event("before_connection")
        await self._old_login(*args, **kwargs)

    async def on_ready(self, *args, **kwargs):
        if not self._on_ready_ran_once:
            await self.execute_event("on_init_complete")
            self._on_ready_ran_once = True
        if self._old_on_ready:
            await self._old_on_ready(*args, **kwargs)
