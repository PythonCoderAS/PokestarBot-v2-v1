if True:  # pragma: coverage
    # discord_slash is ruining the send function! this should stop it...
    import discord
    from discord import http

    original_send = discord.abc.Messageable.send
    original_send_files = http.HTTPClient.send_files
    original_send_message = http.HTTPClient.send_message

    def stop_discord_slash_dpy_overrides():
        discord.abc.Messageable.send = original_send
        discord.http.HTTPClient.send_files = original_send_files
        discord.http.HTTPClient.send_message = original_send_message

    from .models import TORTOISE_ORM
    from .bot import PokestarBot
