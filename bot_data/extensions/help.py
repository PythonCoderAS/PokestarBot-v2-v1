import logging
from typing import TYPE_CHECKING, Any, Mapping, Optional, List

import discord.ext.commands

from .cogs import bot_management
from ..funcs import trim_output, SimpleLinkButtonView, ExtendedHelp
from ..sentry.context import HubContext

if TYPE_CHECKING:
    from ..bot import PokestarBot

logger = logging.getLogger(__name__)


class HelpCommand(discord.ext.commands.HelpCommand):
    context: HubContext

    @property
    def clean_prefix(self):
        return self.context.clean_prefix

    def command_not_found(self, string: str):
        return (
            f"The command `{string}` does not exist. View the command list with `"
            f"{self.clean_prefix}help`."
        )

    def subcommand_not_found(self, command: discord.ext.commands.Command, string: str):
        return (
            f"The subcommand `{string}` does not exist for "
            f"`{self.clean_prefix}{command.qualified_name}`. View the subcommand list "
            f"with `{self.clean_prefix}help {command.qualified_name}`."
        )

    async def send_bot_help(
        self,
        mapping: Mapping[
            Optional[discord.ext.commands.Cog], List[discord.ext.commands.Command]
        ],
    ) -> Any:
        embed = discord.Embed(
            title="Bot Help",
            description="View the bot help online at "
            "https://bot.pokestarfan.ga/help/commands.",
        )
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                embed.add_field(
                    name=cog.qualified_name if cog else "None",
                    value=" ".join(f"`{self.clean_prefix}{item}`" for item in filtered),
                )
        return await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog: discord.ext.commands.Cog):
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        embed = discord.Embed(
            title=cog.qualified_name,
            description=trim_output(cog.description),
        )
        view = SimpleLinkButtonView(
            f"{self.context.bot.settings.bot_settings.base_domain}/cogs/"
            f"{cog.qualified_name}",
            "View Cog Help Online",
        )
        embed.add_field(
            name="Commands",
            value=" ".join(f"`{self.clean_prefix}{item}`" for item in filtered),
        )
        return await self.get_destination().send(embed=embed, view=view)

    async def get_command_help_embed(self, command: discord.ext.commands.Command):
        embed = discord.Embed(title=command.qualified_name)
        embed.add_field(
            name="Syntax",
            value=f"`{self.clean_prefix}{command.qualified_name} {command.signature}`",
        )
        view = ExtendedHelp(self.context.bot.settings.bot_settings.base_domain,
                                   self.context.command)
        return embed, view

    async def send_group_help(self, group: discord.ext.commands.Group):
        filtered = await self.filter_commands(group.commands, sort=True)
        embed, view = await self.get_command_help_embed(group)
        if filtered:
            embed.add_field(
                name="Subcommands",
                value=" ".join(f"`{self.clean_prefix}{item}`" for item in filtered),
            )
        return await self.get_destination().send(embed=embed, view=view)

    async def send_command_help(self, command: discord.ext.commands.Command):
        embed, view = await self.get_command_help_embed(command)
        return await self.get_destination().send(embed=embed, view=view)


help_command = HelpCommand(verify_checks=True)


def setup(bot: "PokestarBot"):
    bot.help_command = help_command
    help_command.cog = bot_management
