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
#     result = races_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Category:
    name: str
    short_name: str
    slug: str
    url: str
    data_url: str
    image: str

    @staticmethod
    def from_dict(obj: Any) -> 'Category':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        short_name = from_str(obj.get("short_name"))
        slug = from_str(obj.get("slug"))
        url = from_str(obj.get("url"))
        data_url = from_str(obj.get("data_url"))
        image = from_str(obj.get("image"))
        return Category(name, short_name, slug, url, data_url, image)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["short_name"] = from_str(self.short_name)
        result["slug"] = from_str(self.slug)
        result["url"] = from_str(self.url)
        result["data_url"] = from_str(self.data_url)
        result["image"] = from_str(self.image)
        return result


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


@dataclass
class Status:
    value: str
    verbose_value: str
    help_text: str

    @staticmethod
    def from_dict(obj: Any) -> 'Status':
        assert isinstance(obj, dict)
        value = from_str(obj.get("value"))
        verbose_value = from_str(obj.get("verbose_value"))
        help_text = from_str(obj.get("help_text"))
        return Status(value, verbose_value, help_text)

    def to_dict(self) -> dict:
        result: dict = {}
        result["value"] = from_str(self.value)
        result["verbose_value"] = from_str(self.verbose_value)
        result["help_text"] = from_str(self.help_text)
        return result


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
    time_limit: str
    category: Category

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
        time_limit = from_str(obj.get("time_limit"))
        category = Category.from_dict(obj.get("category"))
        return Race(name, status, url, data_url, goal, info, entrants_count, entrants_count_inactive, opened_at, started_at, time_limit, category)

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
        result["time_limit"] = from_str(self.time_limit)
        result["category"] = to_class(Category, self.category)
        return result


@dataclass
class Races:
    races: List[Race]

    @staticmethod
    def from_dict(obj: Any) -> 'Races':
        assert isinstance(obj, dict)
        races = from_list(Race.from_dict, obj.get("races"))
        return Races(races)

    def to_dict(self) -> dict:
        result: dict = {}
        result["races"] = from_list(lambda x: to_class(Race, x), self.races)
        return result


def races_from_dict(s: Any) -> Races:
    return Races.from_dict(s)


def races_to_dict(x: Races) -> Any:
    return to_class(Races, x)
