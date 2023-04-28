import discord.ext.commands


class InvalidEnumConversion(discord.ext.commands.BadArgument):
    def __init__(self, enum_name, argument):
        self.name = enum_name
        self.arg = argument
