import platform
import uuid
from typing import Any, Dict, List, Optional, TypeVar, Union

import discord
import sentry_sdk
from asyncdex.utils import remove_prefix
from discord.ext.commands import Context
from sentry_sdk import Scope, init
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.atexit import AtexitIntegration
from sentry_sdk.integrations.dedupe import DedupeIntegration
from sentry_sdk.integrations.excepthook import ExcepthookIntegration
from sentry_sdk.integrations.logging import ignore_logger
from sentry_sdk.integrations.pure_eval import PureEvalIntegration
from sentry_sdk.integrations.stdlib import StdlibIntegration
from sentry_sdk.integrations.threading import ThreadingIntegration

from bot_data.creds import owner_id, sentry_link
from .context import HubContext

ContextType = TypeVar("ContextType", bound=Context)
[ignore_logger(logger_name) for logger_name in ("bot_command_log", "bot_data")]

client = init(
    sentry_link,
    traces_sample_rate=1.0,
    integrations=[
        AioHttpIntegration(transaction_style="method_and_path_pattern"),
        AtexitIntegration(),
        ExcepthookIntegration(),
        DedupeIntegration(),
        StdlibIntegration(),
        ThreadingIntegration(),
        PureEvalIntegration(),
    ],
    environment="testing" if platform.system() == "Darwin" else "production",
    default_integrations=False,
    send_default_pii=True,
    before_send=lambda a, b: a,
    before_breadcrumb=lambda a, b: a,
    in_app_include=["bot_data"],
)


def permission_names(
    permissions: Union[discord.Permissions, discord.PermissionOverwrite]
):
    return ", ".join(name.strip() for name, value in permissions if value)


def context_from_user(
    author: Union[discord.Member, discord.User],
    channel: Optional[discord.abc.GuildChannel] = None,
    *,
    name: str = "user",
) -> Dict[str, Dict[str, Any]]:
    if author:
        perm_name = name + "_permissions"
        derived = {name: {}}
        derived[name]["username"] = f"{author.name}#{author.discriminator}"
        derived[name]["display_name"] = author.display_name
        derived[name]["id"] = author.id
        if isinstance(author, discord.Member):
            top_role: discord.Role = author.top_role
            derived[perm_name] = {}
            derived[perm_name]["top_role"] = top_role.name
            derived[perm_name]["top_role_id"] = top_role.id
            derived[perm_name]["bot_owner"] = author.id == owner_id
            derived[perm_name][
                "is_administrator"
            ] = author.guild_permissions.administrator
            derived[perm_name]["guild_permissions"] = permission_names(
                author.guild_permissions
            )
            author: discord.Member
            if channel:
                derived[perm_name]["channel_permissions"] = permission_names(
                    channel.permissions_for(author)
                )
        return derived
    return {}


def context_from_channel(
    channel: Optional[Union[discord.TextChannel, discord.DMChannel]],
    user: discord.ClientUser,
    *,
    name: str = "channel",
) -> Dict[str, Dict[str, Any]]:
    derived = {}
    if channel:
        guild: discord.Guild = getattr(channel, "guild", None)
        if guild:
            bot_user = guild.me
        else:
            bot_user = user
        derived[name] = {}
        derived[name]["name"] = str(channel)
        derived[name]["id"] = channel.id
        if isinstance(channel, discord.TextChannel):
            derived[name]["nsfw"] = channel.nsfw
            derived[name]["private"] = (
                channel.overwrites_for(guild.default_role).read_messages is True
            )
            derived[name]["category"] = channel.category
        derived[name]["bot_permissions"] = permission_names(
            channel.permissions_for(bot_user)
        )
    return derived


def context_from_voice_channel(
    channel: discord.VoiceChannel, *, name: str = "voice_channel"
) -> Dict[str, Dict[str, Any]]:
    guild: discord.Guild = channel.guild
    bot_user = guild.me
    derived = {name: {}}
    derived[name]["name"] = str(channel)
    derived[name]["id"] = channel.id
    derived[name]["bitrate"] = channel.bitrate
    derived[name]["limit"] = channel.user_limit
    derived[name]["users"] = channel.members
    derived[name]["private"] = (
        channel.overwrites_for(guild.default_role).read_messages is True
    )
    derived[name]["category"] = channel.category
    derived[name]["bot_permissions"] = permission_names(
        channel.permissions_for(bot_user)
    )
    return derived


def context_from_category_channel(
    channel: discord.CategoryChannel, *, name: str = "category_channel"
) -> Dict[str, Dict[str, Any]]:
    guild: discord.Guild = channel.guild
    bot_user = guild.me
    derived = {name: {}}
    derived[name]["name"] = str(channel)
    derived[name]["id"] = channel.id
    derived[name]["private"] = (
        channel.overwrites_for(guild.default_role).read_messages is True
    )
    derived[name]["bot_permissions"] = permission_names(
        channel.permissions_for(bot_user)
    )
    return derived


def context_from_guild(
    guild: Optional[discord.Guild], *, name: str = "guild"
) -> Dict[str, Dict[str, Any]]:
    derived = {}
    if guild:
        bot_user = guild.me
        derived[name] = {}
        derived[name]["name"] = guild.name
        derived[name]["id"] = guild.id
        derived[name]["is_large"] = guild.large
        derived[name]["nitro_boost_level"] = guild.premium_tier
        derived[name]["bot_permissions"] = permission_names(bot_user.guild_permissions)

    return derived


def context_from_message(
    message: Optional[discord.Message], *, name: str = "message"
) -> Dict[str, Dict[str, Any]]:
    derived = {}
    if message:
        message_type: discord.MessageType = message.type
        derived[name] = {}
        derived[name]["id"] = message.id
        derived[name]["timestamp"] = message.created_at
        derived[name]["url"] = message.jump_url
        if message_type:
            derived[name]["type"] = message_type.name
        derived[name]["content"] = message.content
        derived[name]["embed_count"] = len(message.embeds)
        derived[name]["file_count"] = len(message.attachments)
    return derived


def context_from_role(
    role: discord.Role,
    channel: Optional[
        Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel]
    ],
    *,
    name: str = "role",
) -> Dict[str, Dict[str, Any]]:
    derived = {name: {}}
    derived[name]["name"] = role.name
    derived[name]["id"] = role.id
    derived[name]["color"] = hex(role.color.value)[2:].upper()
    derived[name]["members"] = len(role.members)
    derived[name]["position"] = len(role.position)
    derived[name]["permissions"] = permission_names(role.permissions)
    if channel:
        derived[name]["permissions_in_channel_id"] = channel.id
        derived[name]["permissions_in_channel"] = permission_names(
            channel.overwrites_for(role)
        )
    return derived


def get_context_for_object(
    obj: Any,
    client_user: discord.ClientUser,
    suffix: str = "",
    *,
    memo: Optional[List[int]] = None,
    _channel_for_roles: Optional[discord.abc.GuildChannel] = None,
) -> Dict[str, Dict[str, Any]]:
    if memo is None:
        memo = []
    if id(obj) in memo:
        return {}
    if isinstance(obj, (discord.TextChannel, discord.DMChannel)):
        return context_from_channel(obj, client_user, name="channel" + suffix)
    elif isinstance(obj, discord.VoiceChannel):
        return context_from_voice_channel(obj, name="voice_channel" + suffix)
    elif isinstance(obj, discord.CategoryChannel):
        return context_from_category_channel(obj, name="category_channel" + suffix)
    elif isinstance(obj, discord.Guild):
        return context_from_guild(obj, name="guild" + suffix)
    elif isinstance(
        obj, (discord.Member, discord.User, discord.ClientUser, discord.abc.User)
    ):
        return context_from_user(obj, name="user" + suffix)
    elif isinstance(obj, discord.Message):
        return context_from_message(obj, name="message" + suffix)
    elif isinstance(obj, discord.Role):
        return context_from_role(obj, _channel_for_roles, name="role" + suffix)
    elif isinstance(obj, list):
        data = {}
        for num, value in enumerate(obj, start=1):
            data.update(
                get_context_for_object(
                    value,
                    client_user,
                    suffix=suffix + f"_item_{num}",
                    memo=memo,
                    _channel_for_roles=_channel_for_roles,
                )
            )
        return data
    elif isinstance(obj, dict):
        data = {}
        for key, value in obj.items():
            data.update(
                get_context_for_object(
                    value,
                    client_user,
                    suffix=suffix + f"_{key}",
                    memo=memo,
                    _channel_for_roles=_channel_for_roles,
                )
            )
        return data
    else:
        return {}


def extra_context_from_args(
    client_user: discord.ClientUser,
    *args: Any,
    _channel_for_roles: Optional[discord.abc.GuildChannel] = None,
    **kwargs: Any,
) -> Dict[str, Dict[str, Any]]:
    data = {}
    memo = []
    for num, value in enumerate(args, start=1):
        data.update(
            get_context_for_object(
                value,
                client_user,
                suffix=f"_item_{num}",
                memo=memo,
                _channel_for_roles=_channel_for_roles,
            )
        )
    for key, value in kwargs.items():
        data.update(
            get_context_for_object(
                client_user,
                value,
                suffix=f"_{key}",
                memo=memo,
                _channel_for_roles=_channel_for_roles,
            )
        )
    return data


def context_dict_from_context_object(context: HubContext) -> Dict[str, Dict[str, Any]]:
    derived = {"channel": {}}
    author: Union[discord.Member, discord.User] = context.author
    channel: Union[discord.TextChannel, discord.DMChannel] = context.channel
    guild: Optional[discord.Guild] = context.guild
    message: Optional[discord.Message] = context.message
    command: Optional[discord.ext.commands.Command] = context.command
    derived.update(context_from_user(author, channel))
    derived.update(context_from_channel(channel, context.bot.user))
    derived.update(context_from_guild(guild))
    derived.update(context_from_message(message))
    if command:
        derived["command"] = {}
        derived["command"]["name"] = command.qualified_name
        derived["command"]["cog"] = command.cog
        derived["command"]["parent"] = command.parent
        derived["command"]["args"] = context.args
        derived["command"]["kwargs"] = context.kwargs
        if message:
            derived["command"]["args_unparsed"] = remove_prefix(
                message.content, context.prefix + context.invoked_with
            )
        derived["command"]["invoked"] = not context.command_failed
        derived.update(
            extra_context_from_args(context.bot.user, context.args[2:], context.kwargs)
        )
    return derived


def tags_from_values(
    author: Optional[discord.User],
    guild: Optional[discord.Guild],
    channel: Optional[Union[discord.TextChannel, discord.DMChannel]],
    command: Optional[discord.ext.commands.Command],
) -> Dict[str, Union[int, str]]:
    derived = {}
    if author:
        derived["author_id"] = author.id
    if guild:
        derived["guild_id"] = guild.id
    if channel:
        derived["channel_id"] = channel.id
    if command:
        derived["command_name"] = command.qualified_name
    return derived


def tags_from_context(context: HubContext) -> Dict[str, Union[int, str]]:
    return tags_from_values(
        context.author, context.guild, context.channel, context.command
    )


def scope_from_context(
    context: HubContext,
    *,
    extra_context: Optional[Dict[str, Dict[str, Any]]] = None,
    tag_data: Optional[Dict[str, Any]] = None,
) -> Scope:
    if tag_data is None:
        tag_data = {}
    if extra_context is None:
        extra_context = {}
    if isinstance(context, HubContext):
        scope_manager = context.hub.push_scope()
    else:
        scope_manager = sentry_sdk.push_scope()
    scope = scope_manager.__enter__()
    if context:
        if isinstance(context, HubContext):
            original_context = context
            tag_data = {**tags_from_context(original_context), **tag_data}
            context = context_dict_from_context_object(original_context)
            user: Union[discord.Member, discord.User] = original_context.author
            scope.set_user(
                {"id": user.id, "username": user.name + "#" + user.discriminator}
            )
        context.update(extra_context)
        for key, value in context.items():
            scope.set_context(key, value)
    for key, value in tag_data.items():
        scope.set_tag(key, value)
    return scope_manager


def report_exception(
    exception: BaseException,
    context: Optional[Union[HubContext, Dict[str, Dict[str, Any]]]] = None,
    *,
    hub: Optional[sentry_sdk.Hub] = None,
    extra_context: Optional[Dict[str, Dict[str, Any]]] = None,
    tag_data: Optional[Dict[str, Any]] = None,
    error_id: Optional[str] = None,
):
    error_id = (
        error_id
        or getattr(exception, "__pokestarbot_error_id__", None)
        or str(uuid.uuid4())
    )
    tag_data = tag_data or {}
    tag_data["bot_error_id"] = error_id
    with scope_from_context(
        context, extra_context=extra_context, tag_data=tag_data
    ) as scope:
        scope: Scope
        if isinstance(context, HubContext):
            prefix = context.hub
        else:
            prefix = hub or sentry_sdk
        return prefix.capture_exception(exception, scope=scope)


def report_message(
    message: str,
    context: Optional[Union[HubContext, Dict[str, Dict[str, Any]]]] = None,
    *,
    extra_context: Optional[Dict[str, Dict[str, Any]]] = None,
    tag_data: Optional[Dict[str, Any]] = None,
):
    with scope_from_context(
        context, extra_context=extra_context, tag_data=tag_data
    ) as scope:
        scope: sentry_sdk.Scope
        if isinstance(context, HubContext):
            prefix = context.hub
        else:
            prefix = sentry_sdk
        prefix.capture_message(message, scope=scope)
