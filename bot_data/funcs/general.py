import dataclasses
import os.path
from typing import (
    Any,
    Callable,
    Coroutine,
    List,
    Optional,
    TYPE_CHECKING,
    Tuple,
    TypeVar,
    Union,
    Generic,
    AsyncIterable,
    AsyncGenerator,
    Awaitable,
)

import asyncio
import cachetools

if TYPE_CHECKING:
    pass

_T = TypeVar("_T")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_DT = TypeVar("_DT")


def run_coro_sync(coro: Coroutine[Any, Any, _T]) -> _T:
    # Note: Only use with anything that **does not** require an event loop.
    try:
        next(iter(coro.__await__()))
    except StopIteration as exc:
        return exc.value


async def aenumerate(
    it: AsyncIterable[_T], start: int = 0
) -> AsyncGenerator[Tuple[int, _T], None]:
    current = start
    async for item in it:
        yield current, item
    current += 1


def remove_suffix(suffix: str, string: str) -> str:
    if string[-len(suffix) :] == suffix:
        return string[: -len(suffix)]
    return string


def trim_output(output: str, length: int = 2048) -> str:
    if len(output) > length:
        return output[: length - 3] + "..."
    return output


class _Sentinel:
    __slots__ = ()

    def __bool__(self):
        return False

    def __repr__(self):
        return "<Sentinel>"


def format_coordinating_conjunction(word: str, items: List[str]) -> str:
    """Conjunctions are words that join together other words or groups of words, and
    coordinating conjunctions specifically connect words, phrases, and clauses that
    are of equal importance in the sentence."""
    if len(items) == 2:
        return f"{items[0]} {word} {items[1]}"
    else:
        return "{}, {word} {}".format(", ".join(items[:-1]), items[-1], word=word)


def or_format(items: List[str]) -> str:
    return format_coordinating_conjunction("or", items)


def and_format(items: List[str]) -> str:
    return format_coordinating_conjunction("and", items)


data_block_cache = cachetools.TTLCache(128, 60)


def load_data_block(name: str):
    root = os.path.abspath(
        os.path.join(
            __file__, "..", "..", "html", "data", "hosted", "757973999446655078", "data"
        )
    )
    with open(os.path.join(root, name + ".md"), "r", encoding="utf-8") as f:
        f.readline()
        return f.read().strip()


def get_data_block(name: str):
    return data_block_cache.setdefault(name, load_data_block(name))


class Uninitializeable:
    pass


@dataclasses.dataclass(frozen=True)
class NamespaceGetter(Generic[_T, _KT, _VT]):
    namespace: _T
    getter: Callable[[_T, _KT, _DT], Union[_VT, _DT]]


def resolve_variable_through_namespaces(
    name: str,
    *namespaces: NamespaceGetter[Any, str, _VT],
    default: Optional[_DT] = None,
) -> Union[_VT, _DT]:
    for namespace in namespaces:
        val = namespace.getter(namespace.namespace, name, default)
        if val is not default:
            return val
    return default


def repr_template(
    obj: object,
    *attrs: str,
    opening_symbol="<",
    closing_symbol=">",
    **named_attrs: str,
):
    actual_values = {}
    for attr in attrs:
        actual_values[attr] = repr(getattr(obj, attr))
    for name, attr in named_attrs.items():
        actual_values[name] = repr(getattr(obj, attr))
    attrs_str = ", ".join(
        f"{k}={v}" for k, v in sorted(actual_values.items(), key=lambda item: item[0])
    )
    return f"{type(obj).__name__}{opening_symbol}{attrs_str}{closing_symbol}"


class NoReprStr(str):
    def __repr__(self):
        return self


async def do_after(seconds: float, awaitable: Awaitable[_T]) -> _T:
    await asyncio.sleep(seconds)
    return await awaitable
