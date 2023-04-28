import dataclasses
import enum
from typing import Dict, Optional, Union

import discord


class PrivacyLevel(enum.Enum):
    PUBLIC = enum.auto()
    READ_ONLY = enum.auto()
    PRIVATE = enum.auto()


@dataclasses.dataclass()
class SetupChannel:
    name: str
    description: str
    privacy_mode: PrivacyLevel = PrivacyLevel.READ_ONLY
    channel_type: discord.ChannelType = discord.ChannelType.text
    fallback_channel: Optional[str] = "bot-messages"

    def __post_init__(self):
        if isinstance(SetupChannel.channel_type, tuple):
            SetupChannel.channel_type = SetupChannel.channel_type[0]
        if isinstance(self.channel_type, tuple):
            self.channel_type = self.channel_type[0]

    def get_fallback_channel(self) -> Optional["SetupChannel"]:
        if self.fallback_channel is None:
            return
        return setup_constants["Channels"][self.fallback_channel]


@dataclasses.dataclass(frozen=True)
class Option:
    name: str
    description: str
    default: bool = False


@dataclasses.dataclass(frozen=True)
class SetupRole:
    name: str
    description: str
    permission_overwrite: discord.PermissionOverwrite
    fallback_role: Optional[str] = None

    @property
    def permissions_needed(self):
        return self.permission_overwrite.pair()[0]

    def get_fallback_role(self) -> Optional["SetupRole"]:
        if self.fallback_role is None:
            return
        return setup_constants["Roles"][self.fallback_role]


setup_constants: Dict[str, Dict[str, Union[SetupChannel, Option, SetupRole]]] = {
    "Channels": {
        "announcements": SetupChannel(
            "Announcements",
            "The channel that the bot will use to make announcements. Will default to the "
            "the bot-messages channel.",
        ),
        "bot-messages": SetupChannel(
            "Bot Messages",
            "The channel for bot commands.",
            privacy_mode=PrivacyLevel.PUBLIC,
            fallback_channel=None,
        ),
        "admin-log": SetupChannel(
            "Admin Log",
            "The channel to show the invite log and other administrative commands.",
            privacy_mode=PrivacyLevel.PRIVATE,
            fallback_channel=None,
        ),
        "message-goals": SetupChannel(
            "Message Goals",
            "The channel to post when users/channels/the guild reaches a message goal.",
            fallback_channel=None,
        ),
    },
    "Options": {
        "color-on-join": Option(
            "Apply Random Color Role on Join", "Apply a color upon a person joining."
        ),
        "snapshot": Option(
            "Capture User Snapshot",
            "Take a snapshot of the user's roles when they leave.",
            default=True,
        ),
        "expand-reddit-submission": Option(
            "Expand Reddit Submission Links",
            "Show a more detailed view of a submission when a reddit link is posted.",
        ),
        "expand-reddit-comment": Option(
            "Expand Reddit Comment Links",
            "Show a more detailed view of a comment when a reddit link is posted.",
        ),
        "expand-reddit-subreddit": Option(
            "Expand Reddit Subreddit Links",
            "Show a more detailed view of a subreddit when a reddit link is posted.",
        ),
        "expand-reddit-user": Option(
            "Expand Reddit User Links",
            "Show a more detailed view of a user when a reddit link is posted.",
        ),
        "expand-message-txt-files": Option(
            "Expand message.txt Files",
            "Expand any files called message.txt so that mobile users can easily view "
            "the content inside.",
        ),
        "expand-mangadex": Option(
            "Expand MangaDex Links", "Expand any links to MangaDex manga."
        ),
        "expand-guyamoe": Option(
            "Expand Guya.moe Links",
            "Expand any links to Guya.moe manga and manga from similar sites.",
        ),
        "track-invites": Option(
            "Track Invites",
            "Track invites to the server. Requires the admin log channel to be working.",
            default=True,
        ),
    },
    "Roles": {
        "muted": SetupRole(
            "Muted",
            "A role that disallows users from speaking.",
            discord.PermissionOverwrite(send_messages=False, speak=False),
        ),
        "send-all": SetupRole(
            "Send All",
            "A role that allows users to send messages to any channel they can access."
            " Note: This role will never belong to a user for more than 30 seconds,"
            " and it should not give them any further privileges, such as "
            "@everyone permissions.",
            discord.PermissionOverwrite(send_messages=True),
        ),
    },
}
