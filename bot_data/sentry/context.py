from typing import (
    Any,
    Dict,
    List,
    Optional,
    TYPE_CHECKING,
    Union,
)

import discord.ext.commands.view
import sentry_sdk.tracing

from .hub import CustomHub

sentinel = object()

if TYPE_CHECKING:
    from ..bot import PokestarBot
    from ..components.command_error import error_data_type
    from ..funcs import AliasCommand


class HubContext(discord.ext.commands.Context):
    bot: "PokestarBot"
    message: Optional[discord.Message]
    args: List[Any]
    kwargs: Dict[str, Any]
    prefix: Optional[str]
    command: Optional["AliasCommand"]
    view: Optional[discord.ext.commands.view.StringView]
    invoked_with: Optional[str]
    invoked_subcommand: Optional[discord.ext.commands.Command]
    subcommand_passed: Optional[str]
    command_failed: bool

    def set_to_dict(self, name: str, value: Any):
        self.__dict__[name] = value

    @property
    def cog(self) -> Optional[discord.ext.commands.Cog]:
        return super().cog

    @property
    def guild(self) -> Optional[discord.Guild]:
        return super().guild

    @guild.setter
    def guild(self, value: discord.Guild):
        self.set_to_dict("guild", value)

    @property
    def guild_id(self) -> Optional[int]:
        return getattr(self.guild, "id", None)

    @property
    def channel(self) -> Union[discord.TextChannel, discord.DMChannel, discord.Thread]:
        return super().channel

    @channel.setter
    def channel(
        self, value: Union[discord.TextChannel, discord.DMChannel, discord.Thread]
    ):
        self.set_to_dict("channel", value)

    @property
    def author(self) -> Union[discord.Member, discord.User]:
        return super().author

    @author.setter
    def author(self, value: Union[discord.Member, discord.User]):
        self.set_to_dict("author", value)

    @property
    def me(self) -> Union[discord.Member, discord.ClientUser]:
        return super().me

    @me.setter
    def me(self, value: Union[discord.Member, discord.ClientUser]):
        self.set_to_dict("me", value)

    @property
    def voice_client(self) -> Optional[discord.VoiceClient]:
        return super().voice_client

    def __init__(self, **attrs):
        super().__init__(**attrs)
        self.hub = CustomHub(sentry_sdk.Hub.current)
        self.bot.sentry.hubs.append(self.hub)
        self.hub.scope.clear_breadcrumbs()

    async def send(
        self,
        content: Optional[str] = None,
        *,
        embed: Optional[discord.Embed] = None,
        **kwargs
    ):
        kwargs["embed"] = embed
        if self.command and self.message:
            if self.message.channel == self.channel:
                kwargs.setdefault("reference", self.message)
                kwargs.setdefault("mention_author", True)
        return await super().send(content, **kwargs)

    @property
    def message_repr(self):
        from ..funcs import NoReprStr, repr_template

        return NoReprStr(repr_template(self.message, "id"))

    @property
    def channel_repr(self):
        from ..funcs import NoReprStr, repr_template

        return (
            NoReprStr(repr_template(self.channel, "name", "id"))
            if self.message
            else None
        )

    @property
    def guild_repr(self):
        from ..funcs import NoReprStr, repr_template

        return (
            NoReprStr(repr_template(self.guild, "name", "id"))
            if self.message and self.guild
            else None
        )

    @property
    def author_repr(self):
        from ..funcs import NoReprStr, repr_template

        return (
            NoReprStr(
                repr_template(
                    self.author, "name", "id", "discriminator", "display_name"
                )
            )
            if self.message
            else None
        )

    def __repr__(self):
        from ..funcs import repr_template

        return repr_template(
            self,
            "command",
            author="author_repr",
            channel="channel_repr",
            guild="guild_repr",
            message="message_repr",
        )

    @property
    def exception_handlers(self) -> "error_data_type":
        return getattr(self.command, "exception_handlers", {})

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("_"):
            return super().__getattribute__(name)
        val = self.__dict__.get(name, sentinel)
        if val is sentinel:
            return super().__getattribute__(name)
        else:
            return val
