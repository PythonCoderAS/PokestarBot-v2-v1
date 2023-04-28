import discord.ext.commands

from .funcs import AliasCommand
from .sentry.context import HubContext


class CommandConverter(discord.ext.commands.Converter[AliasCommand]):
    async def convert(self, ctx: HubContext, argument: str) -> AliasCommand:
        val = ctx.bot.get_command(argument)
        if val is None:
            await ctx.send(f"The argument `{argument}` is not a valid command.")
            raise discord.ext.commands.BadArgument
        return val
