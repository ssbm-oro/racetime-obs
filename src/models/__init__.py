from typing import Any, List, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime, timedelta
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    if x is None:
        return
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    if x is None:
        return
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    if x is None:
        return
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    if x is None:
        return
    return dateutil.parser.parse(x)

# 'P0DT01H44M03.313433S'
# using an iso 8601 lib to parse this seems like overkill
def from_timedelta(x: Any) -> timedelta:
    if x is None:
        return
    return timedelta(hours= float(x[4:6]), minutes= float(x[7:9]), seconds= float(x[10:-1]))

def from_none(x: Any) -> Any:
    assert x is None
    return x


def to_class(c: Type[T], x: Any) -> dict:
    if x is None:
        return
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    if x is None:
        return
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False

def is_type(t: Type[T], x: Any) -> T:
    if x is None:
        return
    assert isinstance(x, t)
    return x
