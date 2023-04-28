import collections

from . import Component


class Stat(Component):
    """A component that collects statistics on the bot."""

    set_as = "stat"

    def __init__(self, bot):
        super().__init__(bot)
        self._dispatch = bot.dispatcher
        self._send_message = bot.http.send_message
        self._send_files = bot.http.send_files
        self.events = collections.defaultdict(lambda: 0)
        self.messages = 0
        self.files = 0

    async def init_async(self):
        self.bot.dispatcher = self._custom_dispatch
        self.bot.http.send_message = self._custom_send_message
        self.bot.http.send_files = self._custom_send_files

    async def stop_async(self):
        self.bot.dispatcher = self._dispatch
        self.bot.http.send_message = self._send_message
        self.bot.http.send_files = self._send_files

    def _custom_dispatch(self, event_name, *args, **kwargs):
        self.events[event_name] += 1
        return self._dispatch(event_name, *args, **kwargs)

    def _custom_send_message(self, *args, **kwargs):
        self.messages += 1
        return self._send_message(*args, **kwargs)

    def _custom_send_files(self, *args, **kwargs):
        self.files += 1
        return self._send_files(*args, **kwargs)
