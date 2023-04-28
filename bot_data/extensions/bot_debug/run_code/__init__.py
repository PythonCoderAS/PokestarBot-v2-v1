from ....funcs.parse_code_block import parse_discord_code_block


def get_code(item: str):
    if "```" in item:
        return parse_discord_code_block(item)
    else:
        return item.strip()
