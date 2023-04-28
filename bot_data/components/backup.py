import asyncio
import bz2
import io
import os.path
import sys
import tempfile

import discord.ext.tasks

from . import Component
from .sentry import Sentry
from ..creds import bot_support_backup_channel_id


class Backup(Component):
    require = [Sentry]

    async def init_async(self):
        pass

    async def stop_async(self):
        if self.backup_db.is_running():
            self.backup_db.stop()

    @discord.ext.tasks.loop(hours=1)
    async def backup_db(self):
        if sys.platform != "darwin":
            with tempfile.TemporaryDirectory() as temp_dir:
                path = os.path.join(temp_dir, "dump.psql")
                proc = await asyncio.create_subprocess_exec(
                    "pg_dump", "-F", "c", "-f", path, "pokestarbot"
                )
                await proc.wait()
                with open(path, "rb") as file:
                    data: bytes = file.read()
                bio = io.BytesIO(bz2.compress(data))
                await self.bot.get_channel(bot_support_backup_channel_id).send(
                    file=discord.File(bio, "dump.psql.bz2")
                )

    @backup_db.error
    async def backup_db_error(self):
        await self.bot.sentry.on_error("task_backup_db")

    @Component.event
    async def on_init_complete(self):
        self.backup_db.start()
