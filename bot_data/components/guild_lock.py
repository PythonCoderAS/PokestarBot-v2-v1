import discord

from . import Component

guilds = [763375893707882576]

class GuildLock(Component):
    def __init__(self, bot):
        super().__init__(bot)
        self._on_message = self.bot.on_message

    async def init_async(self):
        self.bot.on_message = self.on_message

    async def stop_async(self):
        self.bot.on_message = self._on_message

    async def on_message(self, message: discord.Message):
        guild = message.guild
        if not guild or guild.id in guilds:
            return await self._on_message(message)
