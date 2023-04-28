import discord.ext.commands

from . import debug
from ...sentry.context import HubContext
from ...sentry.view import SentryView


class ReloadView(SentryView):
    def __init__(self, bot: discord.ext.commands.Bot):
        super().__init__()
        self.bot = bot
        self.menu: discord.ui.Select
        self.menu.options = [
            discord.SelectOption(label=item.split(".")[-1], value=item)
            for item in self.bot.extensions.keys()
        ]
        self.menu.max_values = len(self.menu.options)

    @discord.ui.select(placeholder="Extension to Reload")
    async def menu(self, select: discord.ui.Select, interaction: discord.Interaction):
        await interaction.response.defer()
        for value in select.values:
            self.bot.reload_extension(value)
            await interaction.followup.send(f"Reloaded `{value}`.")


@debug.command(aliases=["reload_command"])
async def reload(ctx: HubContext):
    return await ctx.send(
        "Use the menu to reload the extensions.", view=ReloadView(ctx.bot)
    )
