from typing import Optional, TYPE_CHECKING, Union

from discord import (
    CategoryChannel,
    DMChannel,
    Guild,
    Member,
    Role,
    TextChannel,
    User,
    VoiceChannel,
)
from tortoise import fields

if TYPE_CHECKING:
    from ..bot import PokestarBot


class BotMixin:
    bot: Optional["PokestarBot"] = None


class ChannelIdMixin(BotMixin):
    channel_id = fields.BigIntField(null=False)

    @property
    def channel(
        self,
    ) -> Optional[Union[TextChannel, CategoryChannel, VoiceChannel, DMChannel]]:
        if self.channel_id:
            return self.bot.get_channel(self.channel_id)
        return None


class AuthorIdMixin(BotMixin):
    author_id = fields.BigIntField(null=False)

    @property
    def user(self) -> Optional[User]:
        if self.author_id:
            return self.bot.get_user(self.author_id)
        return None

    def is_member(self, guild: Guild) -> bool:
        return isinstance(self.get_member(guild), Member)

    def get_member(self, guild: Guild) -> Optional[Union[Member, User]]:
        if self.author_id:
            return guild.get_member(self.author_id) or self.bot.get_user(self.author_id)
        return None

    @property
    def mention(self) -> str:
        """100% guaranteed to mention them regardless of user/bot status."""
        return f"<@{self.author_id}>"


class RoleMixin(BotMixin):
    role_id = fields.BigIntField(null=False)

    def get_role(self, guild: Guild) -> Optional[Role]:
        if self.role_id:
            return guild.get_role(self.role_id)
        return None
