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
#     result = user_past_races_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


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


class DataURL(Enum):
    ALTTPR_DATA = "/alttpr/data"
    SGL_DATA = "/sgl/data"


class Name(Enum):
    A_LINK_TO_THE_PAST_RANDOMIZER = "A Link to the Past Randomizer"
    SPEED_GAMING_LIVE_2020 = "SpeedGaming Live 2020"


class ShortName(Enum):
    A_LTT_PR = "ALttPR"
    SGL = "SGL"


class Slug(Enum):
    ALTTPR = "alttpr"
    SGL = "sgl"


class URL(Enum):
    ALTTPR = "/alttpr"
    SGL = "/sgl"


@dataclass
class Category:
    name: Name
    short_name: ShortName
    slug: Slug
    url: URL
    data_url: DataURL
    image: str

    @staticmethod
    def from_dict(obj: Any) -> 'Category':
        assert isinstance(obj, dict)
        name = Name(obj.get("name"))
        short_name = ShortName(obj.get("short_name"))
        slug = Slug(obj.get("slug"))
        url = URL(obj.get("url"))
        data_url = DataURL(obj.get("data_url"))
        image = from_str(obj.get("image"))
        return Category(name, short_name, slug, url, data_url, image)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = to_enum(Name, self.name)
        result["short_name"] = to_enum(ShortName, self.short_name)
        result["slug"] = to_enum(Slug, self.slug)
        result["url"] = to_enum(URL, self.url)
        result["data_url"] = to_enum(DataURL, self.data_url)
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
    category: Category
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
        category = Category.from_dict(obj.get("category"))
        ended_at = from_datetime(obj.get("ended_at"))
        cancelled_at = from_none(obj.get("cancelled_at"))
        recordable = from_bool(obj.get("recordable"))
        recorded = from_bool(obj.get("recorded"))
        return Race(name, status, url, data_url, goal, info, entrants_count, entrants_count_inactive, opened_at, started_at, time_limit, category, ended_at, cancelled_at, recordable, recorded)

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
        result["category"] = to_class(Category, self.category)
        result["ended_at"] = self.ended_at.isoformat()
        result["cancelled_at"] = from_none(self.cancelled_at)
        result["recordable"] = from_bool(self.recordable)
        result["recorded"] = from_bool(self.recorded)
        return result


@dataclass
class UserPastRaces:
    count: int
    num_pages: int
    races: List[Race]

    @staticmethod
    def from_dict(obj: Any) -> 'UserPastRaces':
        assert isinstance(obj, dict)
        count = from_int(obj.get("count"))
        num_pages = from_int(obj.get("num_pages"))
        races = from_list(Race.from_dict, obj.get("races"))
        return UserPastRaces(count, num_pages, races)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_int(self.count)
        result["num_pages"] = from_int(self.num_pages)
        result["races"] = from_list(lambda x: to_class(Race, x), self.races)
        return result


def user_past_races_from_dict(s: Any) -> UserPastRaces:
    return UserPastRaces.from_dict(s)


def user_past_races_to_dict(x: UserPastRaces) -> Any:
    return to_class(UserPastRaces, x)
