from dataclasses import dataclass
from typing import Any, Optional, List
from datetime import datetime, timedelta
from models import from_str, from_union, from_none, from_timedelta, from_int, from_bool, from_datetime, from_list
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
    websocket_url: Optional[str] = None
    websocket_bot_url: Optional[str] = None
    websocket_oauth_url: Optional[str] = None

    def get_entrant_by_name(self, full_name : str) -> Entrant:
        entrant = next((x for x in self.entrants if x.user.full_name == full_name), None)
        return entrant

    def get_entrant_by_place(self, place : int) -> Entrant:
        entrant = next((x.finish_time for x in self.entrants if x.place == place), None)
        return entrant


    @staticmethod
    def from_dict(obj: Any) -> 'Race':
        if not isinstance(obj, dict):
            return None
        name = from_str(obj.get("name"))
        #slug = from_str(obj.get("slug"))
        status = Status.from_dict(obj.get("status"))
        url = from_str(obj.get("url"))
        data_url = from_str(obj.get("data_url"))
        websocket_url = from_union([from_str, from_none], obj.get("websocket_url"))
        websocket_bot_url = from_union([from_str, from_none], obj.get("websocket_bot_url"))
        websocket_oauth_url = from_union([from_str, from_none], obj.get("websocket_oauth_url"))
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
        return Race(name=name, status=status, url=url, data_url=data_url, websocket_url=websocket_url, websocket_bot_url=websocket_bot_url, websocket_oauth_url=websocket_oauth_url, category=category, goal=goal, info=info, entrants_count=entrants_count, entrants_count_inactive=entrants_count_inactive, opened_at=opened_at, time_limit=time_limit, entrants=entrants, version=version, started_at=started_at, ended_at=ended_at, cancelled_at=cancelled_at, unlisted=unlisted, streaming_required=streaming_required, auto_start=auto_start, opened_by=opened_by, monitors=monitors, recordable=recordable, recorded=recorded, recorded_by=recorded_by, allow_comments=allow_comments, hide_comments=hide_comments, allow_midrace_chat=allow_midrace_chat, allow_non_entrant_chat=allow_non_entrant_chat, chat_message_delay=chat_message_delay, start_delay=start_delay, entrants_count_finished=entrants_count_finished)


def race_from_dict(s: Any) -> Race:
    return Race.from_dict(s)

def races_from_dict(s: Any) -> List[Race]:
    assert isinstance(s, dict)
    if not s.get("races"):
        return []
    return from_union([lambda x: from_list(Race.from_dict, x), from_none], s.get("races"))