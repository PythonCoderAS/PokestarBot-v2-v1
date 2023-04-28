import asyncio
import code
import contextlib
import io
import pprint
import traceback

from . import Component


class Console(Component):
    set_as = "console"

    def __init__(self, bot):
        super().__init__(bot)
        self.console = code.InteractiveInterpreter(locals=locals())
        self.locals = locals().copy()
        self.code_lock = asyncio.Lock()

    async def init_async(self):
        pass

    async def eval(self, code_to_run: str):
        stdout_io = io.StringIO()
        stderr_io = io.StringIO()
        val = None
        async with self.code_lock:
            with contextlib.redirect_stdout(stdout_io), contextlib.redirect_stderr(
                stderr_io
            ):
                try:
                    val = eval(code_to_run, globals(), self.locals)
                except Exception as e:
                    traceback.print_exception(
                        type(e), e, e.__traceback__.tb_next, file=stderr_io
                    )
        stdout_io.seek(0)
        stderr_io.seek(0)
        return (
            pprint.pformat(val) if val is not None else None,
            stdout_io.read(),
            stderr_io.read(),
        )

    async def exec(self, code_to_run: str):
        async_locals = self.locals.copy()
        formatted = "\n".join(
            " " * 4 + i.expandtabs(4) for i in code_to_run.splitlines(False)
        )
        stdout_io = io.StringIO()
        stderr_io = io.StringIO()
        val = None
        async with self.code_lock:
            with contextlib.redirect_stdout(stdout_io), contextlib.redirect_stderr(
                stderr_io
            ):
                try:
                    exec(
                        f"async def pokestarbot_run_func_async(self):\n{formatted}",
                        globals(),
                        async_locals,
                    )
                    val = await async_locals["pokestarbot_run_func_async"](self)
                except Exception as e:
                    traceback.print_exception(
                        type(e), e, e.__traceback__.tb_next, file=stderr_io
                    )
        stdout_io.seek(0)
        stderr_io.seek(0)
        return (
            pprint.pformat(val) if val is not None else None,
            stdout_io.read(),
            stderr_io.read(),
        )

    async def exec_bash(self, code_to_run: str):
        stdin_io = io.StringIO(code_to_run)
        stdin_io.seek(0)
        stdout_io = io.StringIO()
        stderr_io = io.StringIO()
        await asyncio.create_subprocess_shell(
            "bash", stdin=stdin_io, stdout=stdout_io, stderr=stderr_io
        )
        stdout_io.seek(0)
        stderr_io.seek(0)
        return stdout_io.read(), stderr_io.read()
