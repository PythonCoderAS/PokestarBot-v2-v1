import uuid
from typing import (
    Coroutine,
    Any,
    Optional,
    MutableMapping,
    Callable,
    Iterator,
    Dict,
    Union,
)

import discord.ext.commands

from ..sentry.view import SentryView


class BotContainingView(SentryView):
    def __init__(self, *args, bot: discord.ext.commands.Bot, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    async def on_error(
        self, error: Exception, item: discord.ui.Item, interaction: discord.Interaction
    ) -> None:
        error_id = error.__pokestarbot_error_id__ = str(uuid.uuid4())
        if not interaction.response._responded:
            await interaction.response.defer()
        await self.bot.command_error.send_error_message(
            interaction.followup.send, error_id
        )
        return await super().on_error(error, item, interaction)


class SingleAuthorView(SentryView):
    def __init__(self, *args, original_author_id: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_author_id = original_author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.original_author_id


class Confirmation(SingleAuthorView):
    def __init__(self, coro: Coroutine[Any, Any, Any], original_author_id: int):
        super().__init__(original_author_id=original_author_id)
        self.coro = coro

    async def change_buttons(self, interaction: discord.Interaction):
        self.do_yes.disabled = True
        self.do_no.disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger)
    async def do_yes(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        await self.change_buttons(interaction)
        return await self.coro

    @discord.ui.button(label="No", style=discord.ButtonStyle.success)
    async def do_no(self, _button: discord.ui.Button, interaction: discord.Interaction):
        await self.change_buttons(interaction)


class ShowTextView(SentryView):
    def __init__(self, label: str, text: Optional[str] = None, *embeds: discord.Embed):
        super().__init__()
        embeds = embeds or None
        if text is None and embeds is None:
            raise ValueError("Either 'text' or 'embed' must be specified.")
        self.text = text
        self.embeds = embeds
        self.do_action: discord.ui.Button
        self.do_action.label = label

    @discord.ui.button(label="<PlaceHolder>")
    async def do_action(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        return await interaction.response.send_message(
            content=self.text,
            embeds=list(self.embeds) if self.embeds else None,
            ephemeral=True,
        )


class ShowDebugInfoView(ShowTextView):
    def __init__(self, text: Optional[str] = None, *embeds: discord.Embed):
        super().__init__("Show Debug Info", text, *embeds)


class SimpleLinkButtonView(SentryView):
    def __init__(self, link: str, text: str):
        super().__init__()
        self.button = discord.ui.Button(url=link, label=text, row=4)
        self.add_item(self.button)


_SelectCallableType = Callable[
    [str, discord.Interaction, "SimpleSelectView"], Coroutine[Any, Any, Any]
]


class SimpleSelectView(
    SentryView, MutableMapping[discord.SelectOption, _SelectCallableType]
):
    def __init__(self, *args, placeholder: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.selector.options = []
        self.select_data: Dict[str, _SelectCallableType] = {}
        self.value_to_select_option: Dict[str, discord.SelectOption] = {}
        if placeholder:
            self.selector.placeholder = placeholder

    @discord.ui.select(options=[])
    async def selector(
        self, select: discord.ui.Select, interaction: discord.Interaction
    ):
        label = select.values[0]
        return await self.select_data[label](label, interaction, self)

    def __setitem__(self, k: discord.SelectOption, v: _SelectCallableType):
        self.select_data[k.value] = v
        self.value_to_select_option[k.value] = k
        self.selector.options.append(k)

    def __delitem__(self, v: discord.SelectOption):
        del self.select_data[v.value]
        del self.value_to_select_option[v.value]
        self.selector.options.remove(v)

    def __getitem__(self, k: Union[discord.SelectOption, str]) -> _SelectCallableType:
        return self.select_data[k.value if isinstance(k, discord.SelectOption) else k]

    def __len__(self) -> int:
        return len(self.select_data)

    def __iter__(self) -> Iterator[discord.SelectOption]:
        return iter(self.selector.options)

class ExtendedHelp(SimpleLinkButtonView):
    def __init__(self, base_domain: str, command: discord.ext.commands.Command):
        super().__init__(f"{base_domain}/commands/"
                         f"{command.qualified_name.replace(' ', '/')}",
            "View Detailed Command Help Online")

class ExtendedViewHelp(SimpleLinkButtonView):
    def __init__(self, base_domain: str, command: discord.ext.commands.Command):
        super().__init__(f"{base_domain}/commands/"
                         f"{command.qualified_name.replace(' ', '/')}#interactive-menu",
            "View Detailed View Help Online")
