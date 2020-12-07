# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = category_past_races_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Goal:
    name: str
    custom: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Goal':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        custom = from_bool(obj.get("custom"))
        return Goal(name, custom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["custom"] = from_bool(self.custom)
        return result


class HelpText(Enum):
    THIS_RACE_HAS_BEEN_COMPLETED = "This race has been completed"


class Value(Enum):
    FINISHED = "finished"


class VerboseValue(Enum):
    FINISHED = "Finished"


@dataclass
class Status:
    value: Value
    verbose_value: VerboseValue
    help_text: HelpText

    @staticmethod
    def from_dict(obj: Any) -> 'Status':
        assert isinstance(obj, dict)
        value = Value(obj.get("value"))
        verbose_value = VerboseValue(obj.get("verbose_value"))
        help_text = HelpText(obj.get("help_text"))
        return Status(value, verbose_value, help_text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["value"] = to_enum(Value, self.value)
        result["verbose_value"] = to_enum(VerboseValue, self.verbose_value)
        result["help_text"] = to_enum(HelpText, self.help_text)
        return result


class TimeLimit(Enum):
    P1_DT00_H00_M00_S = "P1DT00H00M00S"


@dataclass
class Race:
    name: str
    status: Status
    url: str
    data_url: str
    goal: Goal
    info: str
    entrants_count: int
    entrants_count_inactive: int
    opened_at: datetime
    started_at: datetime
    time_limit: TimeLimit
    ended_at: datetime
    cancelled_at: None
    recordable: bool
    recorded: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Race':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        status = Status.from_dict(obj.get("status"))
        url = from_str(obj.get("url"))
        data_url = from_str(obj.get("data_url"))
        goal = Goal.from_dict(obj.get("goal"))
        info = from_str(obj.get("info"))
        entrants_count = from_int(obj.get("entrants_count"))
        entrants_count_inactive = from_int(obj.get("entrants_count_inactive"))
        opened_at = from_datetime(obj.get("opened_at"))
        started_at = from_datetime(obj.get("started_at"))
        time_limit = TimeLimit(obj.get("time_limit"))
        ended_at = from_datetime(obj.get("ended_at"))
        cancelled_at = from_none(obj.get("cancelled_at"))
        recordable = from_bool(obj.get("recordable"))
        recorded = from_bool(obj.get("recorded"))
        return Race(name, status, url, data_url, goal, info, entrants_count, entrants_count_inactive, opened_at, started_at, time_limit, ended_at, cancelled_at, recordable, recorded)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["status"] = to_class(Status, self.status)
        result["url"] = from_str(self.url)
        result["data_url"] = from_str(self.data_url)
        result["goal"] = to_class(Goal, self.goal)
        result["info"] = from_str(self.info)
        result["entrants_count"] = from_int(self.entrants_count)
        result["entrants_count_inactive"] = from_int(self.entrants_count_inactive)
        result["opened_at"] = self.opened_at.isoformat()
        result["started_at"] = self.started_at.isoformat()
        result["time_limit"] = to_enum(TimeLimit, self.time_limit)
        result["ended_at"] = self.ended_at.isoformat()
        result["cancelled_at"] = from_none(self.cancelled_at)
        result["recordable"] = from_bool(self.recordable)
        result["recorded"] = from_bool(self.recorded)
        return result


@dataclass
class CategoryPastRaces:
    count: int
    num_pages: int
    races: List[Race]

    @staticmethod
    def from_dict(obj: Any) -> 'CategoryPastRaces':
        assert isinstance(obj, dict)
        count = from_int(obj.get("count"))
        num_pages = from_int(obj.get("num_pages"))
        races = from_list(Race.from_dict, obj.get("races"))
        return CategoryPastRaces(count, num_pages, races)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_int(self.count)
        result["num_pages"] = from_int(self.num_pages)
        result["races"] = from_list(lambda x: to_class(Race, x), self.races)
        return result


def category_past_races_from_dict(s: Any) -> CategoryPastRaces:
    return CategoryPastRaces.from_dict(s)


def category_past_races_to_dict(x: CategoryPastRaces) -> Any:
    return to_class(CategoryPastRaces, x)
