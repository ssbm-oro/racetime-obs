# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = category_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, Callable, cast
from models import *
from models.user import User


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
class CurrentRace:
    name: Optional[str] = None
    status: Optional[Status] = None
    url: Optional[str] = None
    data_url: Optional[str] = None
    goal: Optional[Goal] = None
    info: Optional[str] = None
    entrants_count: Optional[int] = None
    entrants_count_inactive: Optional[int] = None
    opened_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    time_limit: Optional[timedelta] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CurrentRace':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        status = from_union([Status.from_dict, from_none], obj.get("status"))
        url = from_union([from_str, from_none], obj.get("url"))
        data_url = from_union([from_str, from_none], obj.get("data_url"))
        goal = from_union([Goal.from_dict, from_none], obj.get("goal"))
        info = from_union([from_str, from_none], obj.get("info"))
        entrants_count = from_union([from_int, from_none], obj.get("entrants_count"))
        entrants_count_inactive = from_union([from_int, from_none], obj.get("entrants_count_inactive"))
        opened_at = from_union([from_datetime, from_none], obj.get("opened_at"))
        started_at = from_union([from_datetime, from_none], obj.get("started_at"))
        time_limit = from_union([from_timedelta, from_none], obj.get("time_limit"))
        return CurrentRace(name, status, url, data_url, goal, info, entrants_count, entrants_count_inactive, opened_at, started_at, time_limit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["status"] = from_union([lambda x: to_class(Status, x), from_none], self.status)
        result["url"] = from_union([from_str, from_none], self.url)
        result["data_url"] = from_union([from_str, from_none], self.data_url)
        result["goal"] = from_union([lambda x: to_class(Goal, x), from_none], self.goal)
        result["info"] = from_union([from_str, from_none], self.info)
        result["entrants_count"] = from_union([from_int, from_none], self.entrants_count)
        result["entrants_count_inactive"] = from_union([from_int, from_none], self.entrants_count_inactive)
        result["opened_at"] = from_union([lambda x: x.isoformat(), from_none], self.opened_at)
        result["started_at"] = from_union([lambda x: x.isoformat(), from_none], self.started_at)
        result["time_limit"] = from_union([from_str, from_none], self.time_limit)
        return result

@dataclass
class Category:
    name: str
    short_name: str
    slug: str
    url: str
    data_url: str
    image: str
    info: str
    streaming_required: bool
    owners: List[User]
    moderators: List[User]
    goals: List[str]
    current_races: List[CurrentRace]

    @staticmethod
    def from_dict(obj: Any) -> 'Category':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        short_name = from_str(obj.get("short_name"))
        slug = from_str(obj.get("slug"))
        url = from_str(obj.get("url"))
        data_url = from_str(obj.get("data_url"))
        image = from_str(obj.get("image"))
        info = from_str(obj.get("info"))
        streaming_required = from_bool(obj.get("streaming_required"))
        owners = from_list(User.from_dict, obj.get("owners"))
        moderators = from_list(User.from_dict, obj.get("moderators"))
        goals = from_list(from_str, obj.get("goals"))
        current_races = from_list(CurrentRace.from_dict, obj.get("current_races"))
        return Category(name, short_name, slug, url, data_url, image, info, streaming_required, owners, moderators, goals, current_races)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["short_name"] = from_str(self.short_name)
        result["slug"] = from_str(self.slug)
        result["url"] = from_str(self.url)
        result["data_url"] = from_str(self.data_url)
        result["image"] = from_str(self.image)
        result["info"] = from_str(self.info)
        result["streaming_required"] = from_bool(self.streaming_required)
        result["owners"] = from_list(lambda x: to_class(User, x), self.owners)
        result["moderators"] = from_list(lambda x: to_class(User, x), self.moderators)
        result["goals"] = from_list(from_str, self.goals)
        result["current_races"] = from_list(lambda x: to_class(CurrentRace, x), self.current_races)
        return result


def category_from_dict(s: Any) -> Category:
    return Category.from_dict(s)


def category_to_dict(x: Category) -> Any:
    return to_class(Category, x)

