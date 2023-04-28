from typing import Optional

import discord

from ....pager import Paginator
from ....sentry.view import SentryView


class CodeView(SentryView):
    def __init__(
        self, output: Optional[str], stdout: str, stderr: str, time_elapsed: float
    ):
        super().__init__()
        self.output_pager = (
            None
            if not output
            else Paginator.from_lines(
                discord.Embed(title="Output"), output.splitlines(False)
            )
        )
        self.stdout_pager = (
            None
            if not stdout
            else Paginator.from_lines(
                discord.Embed(title="Stdout"), stdout.splitlines(False)
            )
        )
        self.stderr_pager = (
            None
            if not stderr
            else Paginator.from_lines(
                discord.Embed(title="Stderr"), stderr.splitlines(False)
            )
        )
        self.time_elapsed = time_elapsed
        self.change_button_state()

    @discord.ui.button(label="Output")
    async def on_output(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        return await self.output_pager.send_via_method(
            interaction.response.send_message
        )

    @discord.ui.button(label="Stdout")
    async def on_stdout(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        return await self.stdout_pager.send_via_method(
            interaction.response.send_message
        )

    @discord.ui.button(label="Stderr")
    async def on_stderr(
        self, _button: discord.ui.Button, interaction: discord.Interaction
    ):
        return await self.stderr_pager.send_via_method(
            interaction.response.send_message
        )

    def change_button_state(self):
        if not self.output_pager:
            self.on_output.disabled = True
        if not self.stdout_pager:
            self.on_stdout.disabled = True
        if not self.stderr_pager:
            self.on_stderr.disabled = True

    async def send(self, msgable: discord.abc.Messageable):
        await msgable.send(
            f"Code fragment ran in {self.time_elapsed:.3f} seconds.", view=self
        )
        if (self.output_pager, self.stdout_pager, self.stderr_pager).count(None) == 2:
            await (self.output_pager or self.stdout_pager or self.stderr_pager).send(
                msgable
            )
