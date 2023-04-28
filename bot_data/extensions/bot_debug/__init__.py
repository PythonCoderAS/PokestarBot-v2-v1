from typing import TYPE_CHECKING, Optional

import discord.ext.commands

from ..cogs import bot_management, BotManagement, add_cog_to_command
from ...funcs import (
    AliasGroup,
    generate_subcommand_pager,
    FlagTemplate,
)
from ...sentry.context import HubContext

if TYPE_CHECKING:
    from ...bot import PokestarBot


class PagerPageOptions(FlagTemplate):
    text: bool = True
    embed: bool = False
    text_template: str = "This is test line #{number}"
    embed_description_template: str = "This is test embed #{number}"


class PagerLinesOptions(FlagTemplate):
    text: bool = False
    text_template: str = "This is test text #{number}"
    line_template: str = "This is test line #{number}"
    embed_title: str = "{number} Test Lines"


class ExceptionOptions(FlagTemplate):
    name: str = "Exception"
    arg: Optional[str] = None


@discord.ext.commands.group(
    cls=AliasGroup, invoke_without_command=True, aliases=["bot_debug"]
)
@discord.ext.commands.is_owner()
async def debug(self: BotManagement, ctx: HubContext):
    return await generate_subcommand_pager(ctx, debug, title="Debug Subcommands")


def setup(bot: "PokestarBot"):
    from .argument_links import argument_links  # noqa
    from .pager import debug_pager  # noqa
    from .exception import debug_exception  # noqa
    from .run_code.eval import debug_eval  # noqa
    from .run_code.exec import debug_exec  # noqa
    from .command_info import command_info  # noqa
    from .reload import reload  # noqa
    from .command_test.command import command_test  # noqa

    bot.add_command(debug)

    for command in [debug, *debug.walk_commands()]:
        command.add_check(discord.ext.commands.is_owner())

    add_cog_to_command(debug, bot_management)
