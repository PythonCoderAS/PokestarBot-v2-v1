# import os
# from os.path import abspath, join

import ssl

from tortoise import Tortoise

from .statistic import Statistic, StatsChannel

ctx = ssl.create_default_context()
# And in this example we disable validation...
# Please don't do this. Loot at the official Python ``ssl`` module documentation
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_REQUIRED

TORTOISE_ORM = {
    "connections": {
        "default": "postgres://pokestarbot@localhost/pokestarbot",
        # "ubuntuserver": {
        #     "engine": "tortoise.backends.asyncpg",
        #     "credentials": {
        #         "database": "pokestarbot",
        #         "host": "ubuntuserver.lan",
        #         "port": 5432,
        #         "user": "pokestarbot",
        #         "password": None,
        #         "ssl": ctx
        #     }
        # }
    },
    "apps": {
        "models": {
            "models": [__name__, "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "maxsize": 20,
}
"""The config file containing the tortoise ORM setup data."""


async def init():
    """Initialize the ORM."""
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(TORTOISE_ORM)
    # Generate the schema
    await Tortoise.generate_schemas()
