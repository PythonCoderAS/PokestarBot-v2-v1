import datetime
import os

import pytz

from . import Component
from .default_settings import DefaultSettings
from .webserver import WebServer


class Timezone(Component):
    set_as = "tz"

    require = [DefaultSettings, WebServer]

    async def init_async(self):
        os.environ["TIMEZONE"] = self.bot.settings.bot_settings.timezone

    @property
    def tz(self):
        return pytz.timezone(self.bot.settings.bot_settings.timezone)

    @staticmethod
    def current_timestamp():
        return int(datetime.datetime.now(pytz.utc).timestamp())

    def time_format(self, timestamp: int):
        return (
            datetime.datetime.fromtimestamp(timestamp, pytz.utc)
            .astimezone(self.tz)
            .strftime("%B %d %Y at %I:%M:%S %p %Z")
        )
