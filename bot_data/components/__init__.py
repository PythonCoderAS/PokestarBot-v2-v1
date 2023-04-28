import abc
import asyncio
import types
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Type

if TYPE_CHECKING:
    from ..bot import PokestarBot


class Component(abc.ABC):
    """A Component. This defines methods that can be present and must be present in component classes."""

    # If this value is not None, the bot will set an attribute to the component class.
    set_as: Optional[str] = None

    # If this value is not None, the component will not be loaded until the components that are in the list are loaded.
    require: List[Type["Component"]] = list()

    @classmethod
    def event(
        cls, func: Optional[Callable[[], Any]] = None, *, name: Optional[str] = None
    ) -> Callable[[], Any]:
        """Mark a function as an event function.

        :param func: The function to wrap.
        :type func: Callable
        :param name: The name of the event. If not given, it will be guessed from the function.
        :type name: str
        :return: The function.
        :rtype: Callable
        """
        return cls._event_inner(func, name)

    def event_instance(
        self, func: Optional[types.MethodType] = None, *, name: Optional[str] = None
    ):
        self._event_inner(func.__func__, name)
        self.reload_events()

    @staticmethod
    def _event_inner(function, name):
        def wraps(func: Callable[[], Any]) -> Callable[[], Any]:
            func.__component_event__ = True
            if name:
                func.__component_name__ = name
            else:
                func.__component_name__ = func.__name__
            return func

        if function is not None:
            return wraps(function)
        return wraps

    def __init__(self, bot: "PokestarBot"):
        """Do something when the class is created with the bot."""
        self.bot: "PokestarBot" = bot
        self.events: Dict[str, Callable[[], Any]] = {}
        self.reload_events()

    def reload_events(self):
        self.events: Dict[str, Callable[[], Any]] = {}
        for item in dir(self):
            val = getattr(self, item)
            if hasattr(val, "__component_event__"):
                self.events[val.__component_name__] = val

    @abc.abstractmethod
    async def init_async(self):
        """Do all async work needed to initalize the component."""

    async def stop_async(self):
        """Do all async work needed to close the component."""

    async def execute_event(self, name: str):
        return await asyncio.gather(
            *[
                item.events[name]()
                for item in self.bot.components.values()
                if name in item.events
            ]
        )


component_class = None
