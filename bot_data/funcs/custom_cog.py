import re

import discord.ext.commands

from bot_data.funcs import repr_template

pat = re.compile(r"\s+")


class CustomCog(discord.ext.commands.Cog):
    def __init__(self):
        super().__init__()
        self.description = pat.sub(" ", self.description)

    @property
    def children(self) -> int:
        return len(self.get_commands())

    def __repr__(self) -> str:
        return repr_template(self, "description", "children", name="qualified_name")
