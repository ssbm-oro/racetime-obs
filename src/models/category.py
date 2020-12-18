from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, List, Optional

from models import (from_bool, from_datetime, from_int, from_list, from_none,
                    from_str, from_timedelta, from_union)
from models.race import Goal, Status
from models.user import User


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
        if not isinstance(obj, dict):
            return None
        name = from_union([from_str, from_none], obj.get("name"))
        status = from_union([Status.from_dict, from_none], obj.get("status"))
        url = from_union([from_str, from_none], obj.get("url"))
        data_url = from_union([from_str, from_none], obj.get("data_url"))
        goal = from_union([Goal.from_dict, from_none], obj.get("goal"))
        info = from_union([from_str, from_none], obj.get("info"))
        entrants_count = from_union(
            [from_int, from_none], obj.get("entrants_count"))
        entrants_count_inactive = from_union(
            [from_int, from_none], obj.get("entrants_count_inactive"))
        opened_at = from_union(
            [from_datetime, from_none], obj.get("opened_at"))
        started_at = from_union(
            [from_datetime, from_none], obj.get("started_at"))
        time_limit = from_union(
            [from_timedelta, from_none], obj.get("time_limit"))
        return CurrentRace(
            name=name, status=status, url=url, data_url=data_url, goal=goal,
            info=info, entrants_count=entrants_count,
            entrants_count_inactive=entrants_count_inactive,
            opened_at=opened_at, started_at=started_at, time_limit=time_limit
        )


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
        current_races = from_list(
            CurrentRace.from_dict, obj.get("current_races"))
        return Category(
            name=name, short_name=short_name, slug=slug, url=url,
            data_url=data_url, image=image, info=info,
            streaming_required=streaming_required, owners=owners,
            moderators=moderators, goals=goals, current_races=current_races
        )


def category_from_dict(s: Any) -> Category:
    return Category.from_dict(s)
