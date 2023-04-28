from typing import TypeVar, MutableMapping, Dict, Iterator, Callable

_VT = TypeVar("_VT")


class AttrDict(MutableMapping[str, _VT]):
    __slots__ = ("data",)

    def __init__(self):
        self.data: Dict[str, _VT] = dict()

    def __setitem__(self, k: str, v: _VT) -> None:
        self.data[k] = v

    def __delitem__(self, v: str):
        del self.data[v]

    def __getitem__(self, k: str) -> _VT:
        return self.data[k]

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[str]:
        return iter(self.data)

    def __getattr__(self, item: str):
        try:
            return self.data[item]
        except KeyError:
            return self.__getattribute__(item)

    def __setattr__(self, key: str, value: _VT):
        if key == "data":
            return super().__setattr__(key, value)
        self.data[key] = value

    def __delattr__(self, item: str):
        del self.data[item]


class DefaultAttrDict(AttrDict[_VT]):
    __slots__ = ("factory",)

    def __init__(self, missing_factory: Callable[[str], _VT]):
        super().__init__()
        self.factory = missing_factory

    def __missing__(self, key: str) -> _VT:
        self[key] = retval = self.factory(key)
        return retval
