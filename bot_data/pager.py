import abc
import asyncio
import collections
import dataclasses
from typing import List, Optional, Sequence, Dict, Any

import discord.ext.commands

from .emoji import Emoji
from .funcs import get_data_block, SendProtocol
from .sentry.view import SentryView


@dataclasses.dataclass()
class Page:
    message: Optional[str] = None
    embed: Optional[discord.Embed] = None


class BasePaginator(SentryView, abc.ABC):
    @property
    @abc.abstractmethod
    def page_count(self):
        raise NotImplementedError

    def __init__(self):
        super().__init__(timeout=300)
        self.current_page = 1
        self.lock = asyncio.Lock()

    def option_from_page_number(self, page_num: int, **kwargs):
        i = page_num
        return discord.SelectOption(
            label=f"Page {i}",
            value=str(i),
            description=f"Go to page {i}",
            # default=i == self.current_page, # Commented out because we want the
            # label to show.
            **kwargs,
        )

    def options_from_page_number(self):
        page_count = self.page_count
        if page_count <= 25:
            return [
                self.option_from_page_number(i)
                for i in range(1, min(page_count, 25) + 1)
            ]
        else:
            current_page = self.current_page
            if page_count - current_page > 12:
                if current_page - 12 >= 1:
                    return (
                        [
                            self.option_from_page_number(i)
                            for i in range(current_page - 12, current_page)
                        ]
                        + [self.option_from_page_number(current_page)]
                        + [
                            self.option_from_page_number(i)
                            for i in range(current_page + 1, current_page + 12 + 1)
                        ]
                    )
                else:
                    return [
                        self.option_from_page_number(i)
                        for i in range(1, min(page_count, 25) + 1)
                    ]
            else:
                pages_needed_until_end = page_count - current_page
                min_page = current_page - (25 - pages_needed_until_end - 1)
                return (
                    [
                        self.option_from_page_number(i)
                        for i in range(min_page, current_page)
                    ]
                    + [self.option_from_page_number(current_page)]
                    + [
                        self.option_from_page_number(i)
                        for i in range(current_page + 1, page_count + 1)
                    ]
                )

    def apply_options_from_page_number(self):
        items = self.options_from_page_number()
        self.move_to.options = items

    def update_button_state(self):
        self.move_back: discord.ui.Button
        self.move_next: discord.ui.Button
        self.move_first: discord.ui.Button
        self.move_last: discord.ui.Button
        if self.current_page == 1:
            self.move_back.disabled = True
            self.move_first.disabled = True
        else:
            self.move_back.disabled = False
            self.move_first.disabled = False
        if self.current_page == self.page_count:
            self.move_next.disabled = True
            self.move_last.disabled = True
        else:
            self.move_next.disabled = False
            self.move_last.disabled = False

    def run_view_state_change(self):
        self.apply_options_from_page_number()
        self.update_button_state()

    def check_page(self, num: int):
        return 1 <= num <= self.page_count

    async def send(self, channel: discord.abc.Messageable) -> discord.Message:
        return await self.send_via_method(channel.send)

    async def send_via_method(self, method: SendProtocol) -> discord.Message:
        self.run_view_state_change()
        return await method(**await self.get_page_kwargs(1), view=self)

    async def set_page_preprocess(
        self, num: int, interaction: discord.Interaction, responded: bool
    ) -> bool:
        send_meth = (
            interaction.followup.send
            if responded
            else interaction.response.send_message
        )
        if not self.check_page(num):
            if self.page_count == 1:
                await send_meth(
                    f"Page {num} is not a valid page! The only valid page number is 1.",
                    ephemeral=True,
                )
            else:
                await send_meth(
                    f"Page {num} is not a valid page! Only whole numbers between 1 and "
                    f"{self.page_count}, inclusive, are valid page numbers.",
                    ephemeral=True,
                )
            return False
        return True

    async def set_page(
        self, num: int, interaction: discord.Interaction, responded: bool = False
    ):
        if await self.set_page_preprocess(num, interaction, responded):
            old_current_page = self.current_page
            self.current_page = num
            self.run_view_state_change()
            try:
                await interaction.response.edit_message(
                    view=self, **await self.get_page_kwargs(num)
                )
            except Exception as e:
                self.current_page = old_current_page
                raise e

    @abc.abstractmethod
    async def get_page_kwargs(self, page: int) -> Dict[str, Any]:
        raise NotImplementedError

    @discord.ui.button(label="First", emoji=Emoji.DOUBLE_LEFT, row=3)
    async def move_first(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        async with self.lock:
            await self.set_page(1, interaction)

    @discord.ui.button(label="Previous", emoji=Emoji.LEFT, row=3)
    async def move_back(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        async with self.lock:
            await self.set_page(self.current_page - 1, interaction)

    @discord.ui.select(placeholder="Page to Go To", row=4)
    async def move_to(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ):
        val = select.values[0]
        async with self.lock:
            return await self.set_page(int(val), interaction)

    @discord.ui.button(label="Next", emoji=Emoji.RIGHT, row=3)
    async def move_next(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        async with self.lock:
            await self.set_page(self.current_page + 1, interaction)

    @discord.ui.button(label="Last", emoji=Emoji.DOUBLE_RIGHT, row=3)
    async def move_last(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        async with self.lock:
            await self.set_page(self.page_count, interaction)

    @discord.ui.button(label="Info", emoji=Emoji.INFO, row=3)
    async def get_info(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.send_message(
            f"Pager: On **{self.current_page}/{self.page_count}** pages"
        )


class Paginator(BasePaginator):
    pages: List[Page]

    @staticmethod
    def split_line(line: str, max_length: int = 2048) -> List[str]:
        words = collections.deque(line.split(" "))
        items = []
        current_item = words.popleft()
        while words:
            word = words.popleft()
            word_parts = collections.deque()
            if len(word) > max_length:
                while word:
                    word_parts.appendleft(word[:max_length])
                    word = word[max_length:]
            if word_parts:
                word_parts.reverse()
                words = word_parts + words
                continue
            transformation = current_item + " " + word
            if len(transformation) > max_length:
                items.append(current_item)
                current_item = word
            else:
                current_item = transformation
        return items

    @classmethod
    def from_lines(cls, embed: discord.Embed, lines: List[str]):
        embeds = []
        current_embed = embed.copy()
        current_embed.description = current_embed.description or ""
        while lines:
            line = lines.pop(0)
            if len(line) > 2048:
                lines = cls.split_line(line) + lines
            if len(current_embed.description + "\n" + line) > 2048:
                embeds.append(current_embed)
                current_embed = embed.copy()
                current_embed.description = current_embed.description or ""
            if not current_embed.description:
                current_embed.description = line
            else:
                current_embed.description += "\n" + line
        embeds.append(current_embed)
        pages = [Page(embed=item) for item in embeds]
        return cls(pages)

    @property
    def page_count(self):
        return len(self.pages)

    def __init__(self, pages: Sequence[Page]):
        super().__init__()
        self.pages = list(pages)
        pages_count = self.page_count
        if pages_count <= 0:
            raise ValueError("Must have at least one page.")

    def apply_footer(self):
        pages_count = self.page_count
        for page_num, item in enumerate(self.pages, start=1):
            if item.embed and not item.embed.footer.text:
                item.embed.set_footer(text=f"Page {page_num}/{pages_count}")

    @property
    def text(self):
        return self.pages[0].message

    @text.setter
    def text(self, value):
        self.pages[0].message = value

    @property
    def embed(self):
        return self.pages[0].embed

    @embed.setter
    def embed(self, value):
        self.pages[0].embed = value

    def add_text_to_all_pages(self, text: str, overwrite: bool = False):
        for page in self.pages:
            if page.message and not overwrite:
                continue
            page.message = text

    def add_embed_to_all_pages(self, embed: discord.Embed, overwrite: bool = False):
        for page in self.pages:
            if page.embed and not overwrite:
                continue
            page.embed = embed.copy()

    async def get_page_kwargs(self, page: int) -> Dict[str, Any]:
        return dict(
            content=self.pages[page - 1].message, embed=self.pages[page - 1].embed
        )
