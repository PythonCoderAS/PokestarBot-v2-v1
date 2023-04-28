from . import Component
from .settings import Settings


class DefaultSettings(Component):
    require = [Settings]

    async def init_async(self):
        settings = self.bot.settings.bot_settings
        for item in settings.items_to_init:
            if item not in settings:
                val = input(f"Enter a value for {item!r}: ")
                settings[item] = val
