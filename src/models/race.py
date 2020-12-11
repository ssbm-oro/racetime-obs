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
#     result = race_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, Optional, List, TypeVar, Type, Callable, cast
from enum import Enum
from datetime import datetime
import dateutil.parser
from . import *
from models.user import User

@dataclass
class RaceCategory:
    name: str
    short_name: str
    slug: str
    url: str
    data_url: str
    image: str

    @staticmethod
    def from_dict(obj: Any) -> 'RaceCategory':
        if not isinstance(obj, dict):
            return None
        name = from_str(obj.get("name"))
        short_name = from_str(obj.get("short_name"))
        slug = from_str(obj.get("slug"))
        url = from_str(obj.get("url"))
        data_url = from_str(obj.get("data_url"))
        image = from_union([from_str, from_none], obj.get("image"))
        return RaceCategory(name, short_name, slug, url, data_url, image)

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
class Status:
    value: str
    verbose_value: str
    help_text: str

    @staticmethod
    def from_dict(obj: Any) -> 'Status':
        if not isinstance(obj, dict):
            return None
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
class Entrant:
    user: User
    status: Status
    has_comment: bool
    stream_live: bool
    stream_override: bool
    actions: List[str]
    score: Optional[int] = None
    finish_time: Optional[timedelta] = None
    finished_at: Optional[datetime] = None
    place: Optional[int] = None
    place_ordinal: Optional[str] = None
    score_change: Optional[int] = None
    comment: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Entrant':
        if not isinstance(obj, dict):
            return None
        user = User.from_dict(obj.get("user"))
        status = Status.from_dict(obj.get("status"))
        finish_time = from_union([from_timedelta, from_none], obj.get("finish_time"))
        finished_at = from_union([from_datetime, from_none], obj.get("finished_at"))
        place = from_union([from_int, from_none], obj.get("place"))
        place_ordinal = from_union([from_str, from_none], obj.get("place_ordinal"))
        score_change = from_union([from_int, from_none], obj.get("score_change"))
        comment = from_union([from_str, from_none], obj.get("comment"))
        has_comment = from_bool(obj.get("has_comment"))
        stream_live = from_bool(obj.get("stream_live"))
        stream_override = from_bool(obj.get("stream_override"))
        actions = from_list(from_str, obj.get("actions"))
        score = from_union([from_int, from_none], obj.get("score"))
        return Entrant(user=user, status=status, finish_time=finish_time, finished_at=finished_at, place=place, place_ordinal=place_ordinal, score_change=score_change, comment=comment, has_comment=has_comment, stream_live=stream_live, stream_override=stream_override, actions=actions, score=score)

    def to_dict(self) -> dict:
        result: dict = {}
        result["user"] = to_class(User, self.user)
        result["status"] = to_class(Status, self.status)
        #result["finish_time"] = from_none(self.finish_time)
        result["finished_at"] = from_union([from_datetime, from_none], self.finished_at)
        result["place"] = from_union([from_int, from_none], self.place)
        result["place_ordinal"] = from_union([from_str, from_none], self.place_ordinal)
        result["score_change"] = from_union([from_int, from_none], self.score_change)
        result["comment"] = from_union([from_str, from_none], self.comment)
        result["has_comment"] = from_bool(self.has_comment)
        result["stream_live"] = from_bool(self.stream_live)
        result["stream_override"] = from_bool(self.stream_override)
        result["actions"] = from_list(from_str, self.actions)
        result["score"] = from_union([from_int, from_none], self.score)
        return result


@dataclass
class Goal:
    name: str
    custom: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Goal':
        if not isinstance(obj, dict):
            return None
        name = from_str(obj.get("name"))
        custom = from_bool(obj.get("custom"))
        return Goal(name, custom)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["custom"] = from_bool(self.custom)
        return result

@dataclass
class Race:
    name: str
    status: Status
    url: str
    data_url: str
    category: RaceCategory
    goal: Goal
    info: str
    entrants_count: int
    entrants_count_inactive: int
    opened_at: datetime
    time_limit: timedelta
    entrants: Optional[List[Entrant]] = None
    version: Optional[int] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    recorded_by: Optional[User] = None
    start_delay: Optional[timedelta] = None
    streaming_required: Optional[bool] = None
    auto_start: Optional[bool] = None
    opened_by: Optional[User] = None
    monitors: Optional[List[User]] = None
    recordable: Optional[bool] = None
    recorded: Optional[bool] = None
    allow_comments: Optional[bool] = None
    hide_comments: Optional[bool] = None
    allow_midrace_chat: Optional[bool] = None
    allow_non_entrant_chat: Optional[bool] = None
    chat_message_delay: Optional[str] = None
    unlisted: Optional[bool] = None
    entrants_count_finished: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Race':
        if not isinstance(obj, dict):
            return None
        name = from_str(obj.get("name"))
        #slug = from_str(obj.get("slug"))
        status = Status.from_dict(obj.get("status"))
        url = from_str(obj.get("url"))
        data_url = from_str(obj.get("data_url"))
        category = RaceCategory.from_dict(obj.get("category"))
        goal = Goal.from_dict(obj.get("goal"))
        info = from_str(obj.get("info"))
        entrants_count = from_int(obj.get("entrants_count"))
        entrants_count_inactive = from_int(obj.get("entrants_count_inactive"))
        entrants = from_union([lambda x: from_list(Entrant.from_dict, x), from_none], obj.get("entrants"))
        opened_at = from_datetime(obj.get("opened_at"))
        start_delay = from_union([from_timedelta, from_none], obj.get("start_delay"))
        started_at = from_union([from_datetime, from_none], (obj.get("started_at")))
        ended_at = from_union([from_datetime, from_none], (obj.get("ended_at")))
        cancelled_at = from_union([from_datetime, from_none], (obj.get("cancelled_at")))
        unlisted = from_union([from_bool, from_none], obj.get("unlisted"))
        time_limit = from_timedelta(obj.get("time_limit"))
        streaming_required = from_union([from_bool, from_none], obj.get("streaming_required"))
        auto_start = from_union([from_bool, from_none], obj.get("auto_start"))
        opened_by = from_union([lambda x: User.from_dict(x), from_none], obj.get("opened_by"))
        monitors = from_union([lambda x: from_list(User.from_dict, x), from_none], obj.get("monitors"))
        recordable = from_union([from_bool, from_none], obj.get("recordable"))
        recorded = from_union([from_bool, from_none], obj.get("recorded"))
        recorded_by = from_union([lambda x: User.from_dict(x), from_none], obj.get("recorded_by"))
        allow_comments = from_union([from_bool, from_none], obj.get("allow_comments"))
        hide_comments = from_union([from_bool, from_none], obj.get("hide_comments"))
        allow_midrace_chat = from_union([from_bool, from_none], obj.get("allow_midrace_chat"))
        allow_non_entrant_chat = from_union([from_bool, from_none], obj.get("allow_non_entrant_chat"))
        chat_message_delay = from_union([from_str, from_none], obj.get("chat_message_delay"))
        version = from_union([from_int, from_none], obj.get("version"))
        entrants_count_finished = from_union([from_int, from_none], obj.get("entrants_count_finished"))
        return Race(name=name, status=status, url=url, data_url=data_url, category=category, goal=goal, info=info, entrants_count=entrants_count, entrants_count_inactive=entrants_count_inactive, opened_at=opened_at, time_limit=time_limit, entrants=entrants, version=version, started_at=started_at, ended_at=ended_at, cancelled_at=cancelled_at, unlisted=unlisted, streaming_required=streaming_required, auto_start=auto_start, opened_by=opened_by, monitors=monitors, recordable=recordable, recorded=recorded, recorded_by=recorded_by, allow_comments=allow_comments, hide_comments=hide_comments, allow_midrace_chat=allow_midrace_chat, allow_non_entrant_chat=allow_non_entrant_chat, chat_message_delay=chat_message_delay, start_delay=start_delay, entrants_count_finished=entrants_count_finished)

    def to_dict(self) -> dict:
        result: dict = {}
        result["version"] = from_int(self.version)
        result["name"] = from_str(self.name)
        #result["slug"] = from_str(self.slug)
        result["status"] = to_class(Status, self.status)
        result["url"] = from_str(self.url)
        result["data_url"] = from_str(self.data_url)
        result["category"] = to_class(RaceCategory, self.category)
        result["goal"] = to_class(Goal, self.goal)
        result["info"] = from_str(self.info)
        result["entrants_count"] = from_int(self.entrants_count)
        result["entrants_count_inactive"] = from_int(self.entrants_count_inactive)
        result["entrants"] = from_list(lambda x: to_class(Entrant, x), self.entrants)
        result["opened_at"] = self.opened_at.isoformat()
        result["start_delay"] = from_str(self.start_delay)
        result["started_at"] = self.started_at.isoformat()
        result["ended_at"] = from_none(self.ended_at)
        result["cancelled_at"] = from_none(self.cancelled_at)
        result["unlisted"] = from_bool(self.unlisted)
        result["time_limit"] = from_str(self.time_limit)
        result["streaming_required"] = from_bool(self.streaming_required)
        result["auto_start"] = from_bool(self.auto_start)
        result["opened_by"] = to_class(User, self.opened_by)
        result["monitors"] = from_list(lambda x: x, self.monitors)
        result["recordable"] = from_bool(self.recordable)
        result["recorded"] = from_bool(self.recorded)
        result["recorded_by"] = from_none(self.recorded_by)
        result["allow_comments"] = from_bool(self.allow_comments)
        result["hide_comments"] = from_bool(self.hide_comments)
        result["allow_midrace_chat"] = from_bool(self.allow_midrace_chat)
        result["allow_non_entrant_chat"] = from_bool(self.allow_non_entrant_chat)
        result["chat_message_delay"] = from_str(self.chat_message_delay)
        return result


def race_from_dict(s: Any) -> Race:
    return Race.from_dict(s)


def race_to_dict(x: Race) -> Any:
    return to_class(Race, x)

def races_from_dict(s: Any) -> List[Race]:
    assert isinstance(s, dict)
    if not s.get("races"):
        return []
    return from_union([lambda x: from_list(Race.from_dict, x), from_none], s.get("races"))