import functools
from typing import (
    Any,
    Optional,
    Union,
    Callable,
    Tuple,
    Mapping,
    List,
)

import discord.ext.commands
import discord_slash

from .alias_command import AliasCommand
from .general import _Sentinel


class AliasGroup(AliasCommand, discord.ext.commands.Group):
    @property
    def callback(self):
        return super().callback

    @callback.setter
    def callback(self, function):
        AliasCommand.callback.__set__(self, function)

        function = self._callback

        # Voodoo magic time:
        # Aself should normally be a context object, but cog commands will have that
        # "self" parameter. We cannot always assume that there will be a self
        # parameter either, so we need to assume both can be present and set "ctx" to
        # a Sentinel value, since None is a valid value to pass to a function.

        @functools.wraps(function)
        async def wrapped(
            aself: Union[discord.ext.commands.Context, Any],
            ctx: Optional[discord.ext.commands.Context] = _Sentinel(),
            *args,
            **kwargs,
        ):
            actual_ctx = (
                ctx
                if isinstance(
                    ctx, (discord.ext.commands.Context, discord_slash.SlashContext)
                )
                else aself
            )

            if isinstance(actual_ctx, discord.ext.commands.Context):
                if actual_ctx.subcommand_passed and not actual_ctx.invoked_subcommand:
                    params = dict(self.params).copy()
                    params.pop("ctx")
                    params.pop("self", None)
                    if len(params) == 0:
                        raise discord.ext.commands.CommandNotFound(
                            f'Command "{self.qualified_name} '
                            f'{actual_ctx.subcommand_passed}" is not found.'
                        )
            if isinstance(ctx, _Sentinel):
                args = (aself, *args)
            else:
                args = (aself, ctx, *args)
            return await function(*args, **kwargs)

        self._callback = wrapped

    def __init__(self, *args, copy_checks: bool = True, **kwargs):
        kwargs["case_insensitive"] = True
        kwargs.setdefault("invoke_without_command", True)
        super().__init__(*args, **kwargs)
        self.can_copy_checks = copy_checks

    def get_repr_args_and_kwargs(self) -> Tuple[List[str], Mapping[str, str]]:
        items = super().get_repr_args_and_kwargs()
        items[0].append("children")
        return items

    @property
    def children(self) -> int:
        return len(self.commands)

    def copy_checks(self, command: AliasCommand):
        for check in self.checks:
            command.add_check(check)

    def command(
        self, *args, **kwargs
    ) -> Callable[[Callable[..., Any]], "AliasCommand"]:
        def decorator(func):
            kwargs.setdefault("parent", self)
            kwargs.setdefault("cls", AliasCommand)
            result = discord.ext.commands.command(*args, **kwargs)(func)
            self.add_command(result)
            if self.can_copy_checks:
                self.copy_checks(result)
            return result

        return decorator

    def group(self, *args, **kwargs) -> Callable[[Callable[..., Any]], "AliasGroup"]:
        def decorator(func):
            kwargs.setdefault("parent", self)
            kwargs.setdefault("cls", AliasGroup)
            result = discord.ext.commands.group(*args, **kwargs)(func)
            self.add_command(result)
            if self.can_copy_checks:
                self.copy_checks(result)
            return result

        return decorator

    def call_subcommand(self, name: str, *args, **kwargs):
        command: discord.ext.commands.Command = self.get_command(name)
        if command is None:
            raise ValueError(f"'{self.qualified_name} {name}' does not exist!")
        return command(*args, **kwargs)
