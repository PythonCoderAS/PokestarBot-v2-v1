import re
from typing import Sequence

import discord.ext.commands

single_line_code_block = re.compile(r"^(?!`{3})([^\n]+)`{3}")


def parse_discord_code_block(
    string: str,
    language_check: bool = True,
    languages: Sequence[str] = ("python", "py"),
) -> str:
    items = []
    code = ""
    encountered_backtick = False
    while string:
        string: str
        if string[:3] == "```":
            if not encountered_backtick:
                encountered_backtick = True
                string = string[3:]
                if match := single_line_code_block.match(string):
                    code_string = match.group(0)
                    temp_code = ""
                    while code_string[:3] != "```":
                        temp_code += code_string[0]
                        code_string = code_string[1:]
                    code += temp_code
                    string = string[len(temp_code) + 3 :]
                    # code = match.group(1)
                    # string = string[len(match.group(0)):]
                    encountered_backtick = False
                    items.append(code.strip())
                    code = ""
                else:
                    language, sep, string = string.partition("\n")
                    if " " in language:
                        code += language + sep
                        continue
                    language = language.lower()
                    if language not in languages and language and language_check:
                        raise discord.ext.commands.BadArgument(
                            "Language has to be Python."
                        )
            else:
                encountered_backtick = False
                string = string[3:]
                items.append(code.strip())
                code = ""
        elif encountered_backtick:
            code += string[0]
            string = string[1:]
        elif not encountered_backtick:
            string = string[1:]
    processed_items = [item for item in items if bool(item.strip())]
    if processed_items and processed_items[0]:
        return processed_items[0]
    else:
        raise discord.ext.commands.BadArgument("No code could be found.")
