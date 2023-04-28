import contextlib
from typing import (
    Optional,
    TYPE_CHECKING,
)

import sentry_sdk.tracing

if TYPE_CHECKING:
    pass


@contextlib.contextmanager
def start_transaction_or_child(
    hub: Optional[sentry_sdk.Hub] = None, **kwargs
) -> sentry_sdk.tracing.Span:
    hub = hub or sentry_sdk.Hub.current
    current_span: Optional[sentry_sdk.tracing.Span] = (
        getattr(hub, "pokestarbot_current_span", None) or hub.scope.span
    )
    if current_span:
        kwargs.pop("name", None)
        span = current_span.start_child(**kwargs)
        hub.pokestarbot_current_span = span
        try:
            with span:
                yield span
        finally:
            hub.pokestarbot_current_span = current_span
    else:
        trans = hub.start_transaction(**kwargs)
        hub.pokestarbot_current_span = trans
        try:
            with trans:
                yield trans
        finally:
            hub.pokestarbot_current_span = None
