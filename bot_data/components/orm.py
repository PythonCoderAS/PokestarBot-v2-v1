from typing import Callable, Coroutine, Any

import aiohttp.web
import tortoise.transactions

from . import Component
from ..models import init


class ORM(Component):
    async def init_async(self):
        await init()

    async def stop_async(self):
        await tortoise.Tortoise.close_connections()

    @Component.event()
    async def before_webserver_load(self):
        self.bot.web.app.middlewares.append(self.safe_transaction_handler)

    @aiohttp.web.middleware
    async def safe_transaction_handler(
        self,
        request: aiohttp.web.Request,
        handler: Callable[
            [aiohttp.web.Request], Coroutine[Any, Any, aiohttp.web.Response]
        ],
    ) -> aiohttp.web.Response:
        transaction = tortoise.transactions.in_transaction()
        await transaction.__aenter__()
        try:
            retval = await handler(request)
        except aiohttp.web.HTTPException:
            await transaction.__aexit__(None, None, None)
            raise
        except BaseException as e:
            await transaction.__aexit__(type(e), e, e.__traceback__)
            raise e
        else:
            await transaction.__aexit__(None, None, None)
            return retval
