"""Contains the Menu class."""
import dataclasses
from typing import Any, Callable, Coroutine, Dict, List, Optional, Union

import discord


@dataclasses.dataclass(unsafe_hash=True)
class MenuItem:
    """A dataclass representing one of the choices in a menu."""

    name: str
    """The name of the item. This will be shown to users."""
    on_select: Callable[[discord.RawReactionActionEvent], Coroutine[Any, Any, Any]]
    """A coroutine that does something when chosen. It is given the message containing the menu and the user that 
    reacted to the emoji that the item represents."""
    emoji: Optional[str] = None
    """The discord emoji code (with the ``:``) or the Unicode emoji to use for this item. If left empty, a numerical 
    emoji will be assigned."""


class Menu(discord.ui.View):
    """A Menu. Each item in the Menu is an instance of :class:`MenuItem`. Each MenuItem is limited to 20 items
    because of Discord reaction limits."""

    text: Optional[str]
    """The text of the menu."""

    embed: Optional[discord.Embed]
    """The embed of the menu."""

    autogenerate: bool
    """Whether or not to create an embed if none is given."""

    title: str
    """The title to use for the autogenerated embed. Defaults to ``Menu``."""

    item_list: List[MenuItem]
    """The list of MenuItems for this menu."""

    emoji_number_mapping: Dict[int, str] = {
        1: "1️⃣",
        2: "2️⃣",
        3: "3️⃣",
        4: "4️⃣",
        5: "5️⃣",
        6: "6️⃣",
        7: "7️⃣",
        8: "8️⃣",
        9: "9️⃣",
        10: "0️⃣",
    }
    """The mapping of numeric numbers to the respective Discord emoji version. """

    def __init__(
        self,
        *items: MenuItem,
        content: Optional[str] = None,
        embed: Optional[discord.Embed] = None,
        autogenerate: bool = False,
        title: str = "Menu",
    ):
        self.text = content
        self.embed = embed
        self.autogenerate = autogenerate
        self.title = title
        item_list = [*items]
        if len(item_list) > 20:
            raise ValueError("There cannot be >20 items in a menu.")
        count = 0
        for item in item_list:
            if item.emoji is None:
                count += 1
                if count > 10:
                    raise ValueError(
                        "There can only be up to 10 un-numbered menu items."
                    )
                else:
                    item.emoji = self.emoji_number_mapping[count]
        self.item_list = item_list
        super().__init__()

    async def post_menu(self, channel: discord.abc.Messageable) -> discord.Message:
        """
        Posts the menu to the specified channel and adds the reactions.

        :param channel: Any object that allows sending messages to it.
        :type channel: discord.abc.Messageable
        :return: The Message object.
        :rtype: discord.Message
        """
        embed = self.embed
        content = self.text
        if self.autogenerate and embed is None:
            embed = discord.Embed(title=self.title)
            temp_str = ""
            for item in self.item_list:
                temp_str += f"{item.emoji}: {item.name}\n"
            embed.description = temp_str.rstrip()
        msg = await channel.send(content=content, embed=embed)
        for item in self.item_list:
            await msg.add_reaction(item.emoji)
        return msg

    async def execute_reaction(self, reaction: discord.RawReactionActionEvent) -> Any:
        """
        Execute a given reaction.

        :param reaction: A RawReactionActionEvent object.
        :type reaction: :class:`discord.RawReactionActionEvent`
        :return: Either the return value of the function that is provided as a callback (may be None) or None
        :rtype: Union[Any, None]
        """
        for item in self.item_list:
            if str(item.emoji) in str(reaction.emoji):
                return await item.on_select(reaction)
        return None
