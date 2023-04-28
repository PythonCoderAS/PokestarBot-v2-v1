import os

from . import Component


class PIDFile(Component):
    async def init_async(self):
        base = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(base, "Pidfile"), "w") as f:
            f.write(str(os.getpid()))

    async def stop_async(self):
        base = os.path.dirname(os.path.dirname(__file__))
        pidfile_path = os.path.join(base, "Pidfile")
        if os.path.exists(pidfile_path):
            os.remove(pidfile_path)
