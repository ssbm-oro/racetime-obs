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


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


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


class Action(Enum):
    DONE = "done"
    FORFEIT = "forfeit"


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
class OpenedBy:
    id: str
    full_name: str
    name: str
    url: str
    flair: str
    twitch_name: str
    twitch_display_name: str
    twitch_channel: str
    can_moderate: bool
    discriminator: Optional[int] = None
    avatar: Optional[str] = None
    pronouns: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'OpenedBy':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        full_name = from_str(obj.get("full_name"))
        name = from_str(obj.get("name"))
        discriminator = from_union([from_none, lambda x: int(from_str(x))], obj.get("discriminator"))
        url = from_str(obj.get("url"))
        flair = from_str(obj.get("flair"))
        twitch_name = from_str(obj.get("twitch_name"))
        twitch_display_name = from_str(obj.get("twitch_display_name"))
        twitch_channel = from_str(obj.get("twitch_channel"))
        can_moderate = from_bool(obj.get("can_moderate"))
        avatar = from_union([from_none, from_str], obj.get("avatar"))
        pronouns = from_union([from_none, from_str], obj.get("pronouns"))
        return OpenedBy(id, full_name, name, discriminator, url, flair, twitch_name, twitch_display_name, twitch_channel, can_moderate, avatar, pronouns)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["full_name"] = from_str(self.full_name)
        result["name"] = from_str(self.name)
        result["discriminator"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.discriminator)
        result["url"] = from_str(self.url)
        result["flair"] = from_str(self.flair)
        result["twitch_name"] = from_str(self.twitch_name)
        result["twitch_display_name"] = from_str(self.twitch_display_name)
        result["twitch_channel"] = from_str(self.twitch_channel)
        result["can_moderate"] = from_bool(self.can_moderate)
        result["avatar"] = from_union([from_none, from_str], self.avatar)
        result["pronouns"] = from_union([from_none, from_str], self.pronouns)
        return result


@dataclass
class Entrant:
    user: OpenedBy
    status: Status
    finish_time: None
    finished_at: None
    place: None
    place_ordinal: None
    score_change: None
    comment: None
    has_comment: bool
    stream_live: bool
    stream_override: bool
    actions: List[Action]
    score: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Entrant':
        assert isinstance(obj, dict)
        user = OpenedBy.from_dict(obj.get("user"))
        status = Status.from_dict(obj.get("status"))
        finish_time = from_none(obj.get("finish_time"))
        finished_at = from_none(obj.get("finished_at"))
        place = from_none(obj.get("place"))
        place_ordinal = from_none(obj.get("place_ordinal"))
        score_change = from_none(obj.get("score_change"))
        comment = from_none(obj.get("comment"))
        has_comment = from_bool(obj.get("has_comment"))
        stream_live = from_bool(obj.get("stream_live"))
        stream_override = from_bool(obj.get("stream_override"))
        actions = from_list(Action, obj.get("actions"))
        score = from_union([from_int, from_none], obj.get("score"))
        return Entrant(user, status, finish_time, finished_at, place, place_ordinal, score_change, comment, has_comment, stream_live, stream_override, actions, score)

    def to_dict(self) -> dict:
        result: dict = {}
        result["user"] = to_class(OpenedBy, self.user)
        result["status"] = to_class(Status, self.status)
        result["finish_time"] = from_none(self.finish_time)
        result["finished_at"] = from_none(self.finished_at)
        result["place"] = from_none(self.place)
        result["place_ordinal"] = from_none(self.place_ordinal)
        result["score_change"] = from_none(self.score_change)
        result["comment"] = from_none(self.comment)
        result["has_comment"] = from_bool(self.has_comment)
        result["stream_live"] = from_bool(self.stream_live)
        result["stream_override"] = from_bool(self.stream_override)
        result["actions"] = from_list(lambda x: to_enum(Action, x), self.actions)
        result["score"] = from_union([from_int, from_none], self.score)
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
class Race:
    version: int
    name: str
    slug: str
    status: Status
    url: str
    data_url: str
    websocket_url: str
    websocket_bot_url: str
    websocket_oauth_url: str
    category: Category
    goal: Goal
    info: str
    entrants_count: int
    entrants_count_inactive: int
    entrants: List[Entrant]
    opened_at: datetime
    start_delay: str
    started_at: datetime
    ended_at: None
    cancelled_at: None
    unlisted: bool
    time_limit: str
    streaming_required: bool
    auto_start: bool
    opened_by: OpenedBy
    monitors: List[Any]
    recordable: bool
    recorded: bool
    recorded_by: None
    allow_comments: bool
    hide_comments: bool
    allow_midrace_chat: bool
    allow_non_entrant_chat: bool
    chat_message_delay: str

    @staticmethod
    def from_dict(obj: Any) -> 'Race':
        assert isinstance(obj, dict)
        version = from_int(obj.get("version"))
        name = from_str(obj.get("name"))
        slug = from_str(obj.get("slug"))
        status = Status.from_dict(obj.get("status"))
        url = from_str(obj.get("url"))
        data_url = from_str(obj.get("data_url"))
        websocket_url = from_str(obj.get("websocket_url"))
        websocket_bot_url = from_str(obj.get("websocket_bot_url"))
        websocket_oauth_url = from_str(obj.get("websocket_oauth_url"))
        category = Category.from_dict(obj.get("category"))
        goal = Goal.from_dict(obj.get("goal"))
        info = from_str(obj.get("info"))
        entrants_count = from_int(obj.get("entrants_count"))
        entrants_count_inactive = from_int(obj.get("entrants_count_inactive"))
        entrants = from_list(Entrant.from_dict, obj.get("entrants"))
        opened_at = from_datetime(obj.get("opened_at"))
        start_delay = from_str(obj.get("start_delay"))
        started_at = from_datetime(obj.get("started_at"))
        ended_at = from_none(obj.get("ended_at"))
        cancelled_at = from_none(obj.get("cancelled_at"))
        unlisted = from_bool(obj.get("unlisted"))
        time_limit = from_str(obj.get("time_limit"))
        streaming_required = from_bool(obj.get("streaming_required"))
        auto_start = from_bool(obj.get("auto_start"))
        opened_by = OpenedBy.from_dict(obj.get("opened_by"))
        monitors = from_list(lambda x: x, obj.get("monitors"))
        recordable = from_bool(obj.get("recordable"))
        recorded = from_bool(obj.get("recorded"))
        recorded_by = from_none(obj.get("recorded_by"))
        allow_comments = from_bool(obj.get("allow_comments"))
        hide_comments = from_bool(obj.get("hide_comments"))
        allow_midrace_chat = from_bool(obj.get("allow_midrace_chat"))
        allow_non_entrant_chat = from_bool(obj.get("allow_non_entrant_chat"))
        chat_message_delay = from_str(obj.get("chat_message_delay"))
        return Race(version, name, slug, status, url, data_url, websocket_url, websocket_bot_url, websocket_oauth_url, category, goal, info, entrants_count, entrants_count_inactive, entrants, opened_at, start_delay, started_at, ended_at, cancelled_at, unlisted, time_limit, streaming_required, auto_start, opened_by, monitors, recordable, recorded, recorded_by, allow_comments, hide_comments, allow_midrace_chat, allow_non_entrant_chat, chat_message_delay)

    def to_dict(self) -> dict:
        result: dict = {}
        result["version"] = from_int(self.version)
        result["name"] = from_str(self.name)
        result["slug"] = from_str(self.slug)
        result["status"] = to_class(Status, self.status)
        result["url"] = from_str(self.url)
        result["data_url"] = from_str(self.data_url)
        result["websocket_url"] = from_str(self.websocket_url)
        result["websocket_bot_url"] = from_str(self.websocket_bot_url)
        result["websocket_oauth_url"] = from_str(self.websocket_oauth_url)
        result["category"] = to_class(Category, self.category)
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
        result["opened_by"] = to_class(OpenedBy, self.opened_by)
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
