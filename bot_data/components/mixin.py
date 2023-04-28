from . import Component
from ..models.mixins import BotMixin


class BotMixinComponent(Component):
    async def init_async(self):
        if not getattr(BotMixin, "bot", None):
            BotMixin.bot = self.bot

    async def stop_async(self):
        BotMixin.bot = None
