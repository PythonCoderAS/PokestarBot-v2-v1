import functools
from typing import Callable, Any, Coroutine

import aiohttp
import sentry_sdk

from . import Component
from .sentry import Sentry
from ..funcs import start_transaction_or_child


class Session(Component):
    set_as = "session"

    require = [Sentry]

    session: aiohttp.ClientSession
    _request: Callable

    async def init_async(self):
        self.session = aiohttp.ClientSession()
        self._request = self.session._request
        self.session._request = functools.partial(self.request_inner, self._request)

    def request(self, method, url, **kwargs):
        return self.session.request(method, url, **kwargs)

    async def request_inner(
        self,
        request_method: Callable[..., Coroutine[Any, Any, Any]],
        method,
        url,
        return_if_hub_is_none: bool = False,
        **kwargs,
    ):
        # How to use this method:
        # This method should replace Sesssion._request. To that end, you should use
        # Session._request = functools.partial(request_inner, Session._request).
        hub = self.bot.sentry.get_hub()
        if hub is None and return_if_hub_is_none:
            return await request_method(method, url, **kwargs)
        else:
            hub = hub or sentry_sdk.Hub.current
        if getattr(hub, "pokestarbot_current_span", None) is None:
            return await request_method(method, url, **kwargs)
        with start_transaction_or_child(
            hub, name=f"{method} {url}", description=f"{method} {url}", op="http"
        ) as span:
            span.set_tag("http_method", method)
            span.set_tag("http_url", url)
            try:
                req = await request_method(method, url, **kwargs)
            except Exception:
                raise
            else:
                span.set_http_status(req.status)
                return req

    async def stop_async(self):
        await self.session.close()
