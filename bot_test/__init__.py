import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(__file__, "..", ".."))
)  # Needed to have our things load in.

if True:  # stop pesky linters
    from bot_data import PokestarBot  # noqa
