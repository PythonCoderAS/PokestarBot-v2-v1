import discord.ext.commands

from . import Component


class DisableHelpComponent(Component):
    async def init_async(self):
        # self.bot.remove_command('help')
        pass

    async def stop_async(self):
        self.bot.help_command = discord.ext.commands.DefaultHelpCommand()
