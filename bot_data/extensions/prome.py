import collections
from typing import Dict, TYPE_CHECKING

import aiohttp.web
import discord.ext.commands
import tortoise
from tortoise.functions import Sum

from ..funcs import AliasCommand
from ..funcs.custom_cog import CustomCog
from ..models import StatsChannel, Statistic
from ..sentry.context import HubContext

if TYPE_CHECKING:
    from ..bot import PokestarBot


class BotDashboard(CustomCog):
    """This cog manages the part of the website that takes data from the bot and
    shows it graphically."""

    @property
    def command_data(self) -> Dict[str, int]:
        return self.bot.command_data

    @property
    def success_command_data(self) -> Dict[str, int]:
        return self.bot.success_command_data

    @property
    def error_command_data(self) -> Dict[str, int]:
        return self.bot.error_command_data

    def __init__(self, bot: "PokestarBot"):
        self.bot = bot
        if not hasattr(bot, "command_data"):
            bot.command_data = collections.defaultdict(lambda: 0)
        if not hasattr(bot, "success_command_data"):
            bot.success_command_data = collections.defaultdict(lambda: 0)
        if not hasattr(bot, "error_command_data"):
            bot.error_command_data = collections.defaultdict(lambda: 0)
        bot.web.add_routes([aiohttp.web.get("/prometheus/metrics", self.report_data)])

    @discord.ext.commands.Cog.listener()
    async def on_command(self, ctx: discord.ext.commands.Context):
        self.command_data[ctx.command.name] += 1

    @discord.ext.commands.Cog.listener()
    async def on_command_completion(self, ctx: discord.ext.commands.Context):
        self.success_command_data[ctx.command.name] += 1

    @discord.ext.commands.Cog.listener()
    async def on_command_error(
        self, ctx: discord.ext.commands.Context, error: BaseException
    ):
        if ctx.command:
            self.error_command_data[ctx.command.name] += 1
        else:
            self.error_command_data["None"] += 1

    async def report_data(self, request):
        data = (
            "# HELP pokestarbot_events The various bot events seen\n# TYPE "
            "pokestarbot_events counter\n"
        )
        for name, value in self.bot.stat.events.items():
            data += 'pokestarbot_events{name="%s"} %.1f\n' % (name, value)
        if self.command_data:
            data += (
                "# HELP pokestarbot_commands The various commands executed\n # "
                "TYPE pokestarbot_commands counter\n"
            )
            for name, value in self.command_data.items():
                data += 'pokestarbot_commands{name="%s"} %.1f\n' % (name, value)
        if self.error_command_data:
            data += (
                "# HELP pokestarbot_commands_failed The various commands that failed\n "
                "# TYPE pokestarbot_commands_failed counter\n"
            )
            for name, value in self.error_command_data.items():
                data += 'pokestarbot_commands_failed{name="%s"} %.1f\n' % (name, value)
        if self.success_command_data:
            data += (
                "# HELP pokestarbot_commands_success The various commands that "
                "succeeded\n # TYPE pokestarbot_commands_success counter\n"
            )
            for name, value in self.success_command_data.items():
                data += 'pokestarbot_commands_success{name="%s"} %.1f\n' % (name, value)
        data += (
            "# HELP metric1 Messages sent in channel in guild\n# TYPE metric1 gauge\n"
        )
        for item in (
            await StatsChannel.annotate(sum=Sum("authors__messages"))
            .group_by("guild_id")
            .values("guild_id", "sum")
        ):
            guild = self.bot.get_guild(item["guild"])
            guild_name = (
                "<Unknown Guild>" if not guild else guild.name.replace('"', r"\"")
            )
            item.update(guild_name=guild_name)
            data += (
                'metric1{guild="%(guild)s",guild_name="%(guild_name)s"} %('
                "num).1f\n" % item
            )
        data += (
            "# HELP pokestarbot_roles The number of roles in a guild\n# TYPE "
            "pokestarbot_roles gauge\n"
        )
        for guild in self.bot.guilds:
            guild: discord.Guild
            data += 'pokestarbot_roles{guild="%s"} %.1f\n' % (
                guild.id,
                len(guild.roles),
            )
        data += (
            "# HELP pokestarbot_members The number of members in a guild\n# TYPE "
            "pokestarbot_members gauge\n"
        )
        for guild in self.bot.guilds:
            guild: discord.Guild
            data += 'pokestarbot_members{guild="%s"} %.1f\n' % (
                guild.id,
                len(guild.members),
            )
        data += (
            "# HELP pokestarbot_channels The number of channels in a guild\n# "
            "TYPE pokestarbot_channels gauge\n"
        )
        for guild in self.bot.guilds:
            guild: discord.Guild
            data += 'pokestarbot_channels{guild="%s",type="text"} %.1f\n' % (
                guild.id,
                len(guild.text_channels),
            )
            data += 'pokestarbot_channels{guild="%s",type="voice"} %.1f\n' % (
                guild.id,
                len(guild.voice_channels),
            )
            data += 'pokestarbot_channels{guild="%s",type="category"} %.1f\n' % (
                guild.id,
                len(guild.categories),
            )
        return aiohttp.web.Response(body=data)

    @discord.ext.commands.command(
        cls=AliasCommand, aliases=["bot_dashboard", "grafana_dashboard", "grafana"]
    )
    @discord.ext.commands.guild_only()
    async def dashboard(self, ctx: HubContext):
        return await ctx.send(
            "Link to the dashboard for the current guild: https://bot.pokestarfan."
            "ga/grafana/d/Z6c2fVMnz/pokestarbot?orgId=1&refresh=30s&var-Guild"
            f"={ctx.guild.id}"
        )


def setup(bot: "PokestarBot"):
    bot.add_cog(BotDashboard(bot))
