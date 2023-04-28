import time

import discord.ext.commands

from bot_data.extensions.bot_debug.run_code import get_code
from .code_view import CodeView
from .. import debug
from ....sentry.context import HubContext


@debug.command(name="exec", aliases=["execute", "exec_code", "execute_code"])
async def debug_exec(ctx: HubContext, *, block: str):
    code_to_use = get_code(block)
    start = time.monotonic()
    output, stdout, stderr = await ctx.bot.console.exec(code_to_use)
    finish = time.monotonic()
    return await CodeView(output, stdout, stderr, finish - start).send(ctx)


@debug_exec.exception_handler(discord.ext.commands.BadArgument)
async def handle_bad_argument(ctx: HubContext, exc: discord.ext.commands.BadArgument):
    if type(exc) is not discord.ext.commands.BadArgument:
        raise exc
    return await ctx.send(exc.args[0])
