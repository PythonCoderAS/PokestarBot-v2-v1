#!/usr/bin/env python3
from distutils.core import setup, Extension

setup(
    name="pokestarbot_c",
    version="1.2",
    ext_modules=[
        Extension("pokestarbot_c", ["bind.c", "libpokestarbot.c", "libminecraftxp.c"])
    ],
)
