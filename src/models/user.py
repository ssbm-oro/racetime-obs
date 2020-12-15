# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = user_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast, Optional
from models import *

@dataclass
class Stats:
    joined: int
    first: int
    second: int
    third: int
    forfeits: int
    dqs: int

    @staticmethod
    def from_dict(obj: Any) -> 'Stats':
        if not isinstance(obj, dict):
            return None
        joined = from_int(obj.get("joined"))
        first = from_int(obj.get("first"))
        second = from_int(obj.get("second"))
        third = from_int(obj.get("third"))
        forfeits = from_int(obj.get("forfeits"))
        dqs = from_int(obj.get("dqs"))
        return Stats(joined, first, second, third, forfeits, dqs)

    def to_dict(self) -> dict:
        result: dict = {}
        result["joined"] = from_int(self.joined)
        result["first"] = from_int(self.first)
        result["second"] = from_int(self.second)
        result["third"] = from_int(self.third)
        result["forfeits"] = from_int(self.forfeits)
        result["dqs"] = from_int(self.dqs)
        return result


@dataclass
class User:
    id: str
    full_name: str
    name: str
    url: str
    discriminator: Optional[str] = None
    stats: Optional[Stats] = None
    pronouns: Optional[str] = None
    flair: Optional[str] = None
    twitch_name: Optional[str] = None
    twitch_display_name: Optional[str] = None
    twitch_channel: Optional[str] = None
    can_moderate: Optional[bool] = None    
    avatar: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        if not isinstance(obj, dict):
            return None
        id = from_str(obj.get("id"))
        full_name = from_str(obj.get("full_name"))
        name = from_str(obj.get("name"))
        discriminator = from_union([from_str, from_none], obj.get("discriminator"))
        url = from_str(obj.get("url"))
        avatar = from_union([from_str, from_none], obj.get("avatar"))
        pronouns = from_union([from_str, from_none], obj.get("pronouns"))
        flair = from_union([from_str, from_none], obj.get("flair"))
        twitch_name = from_union([from_str, from_none], obj.get("twitch_name"))
        twitch_display_name = from_union([from_str, from_none], obj.get("twitch_display_name"))
        twitch_channel = from_union([from_str, from_none], obj.get("twitch_channel"))
        can_moderate = from_union([from_bool, from_none], obj.get("can_moderate"))
        stats = from_union([Stats.from_dict, from_none], obj.get("stats"))
        return User(id=id, full_name=full_name, name=name, discriminator=discriminator, url=url, avatar=avatar, pronouns=pronouns, flair=flair, twitch_name=twitch_name, twitch_display_name=twitch_display_name, twitch_channel=twitch_channel, can_moderate=can_moderate, stats=stats)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["full_name"] = from_str(self.full_name)
        result["name"] = from_str(self.name)
        result["discriminator"] = from_str(self.discriminator)
        result["url"] = from_str(self.url)
        result["avatar"] = from_str(self.avatar)
        result["pronouns"] = from_str(self.pronouns)
        result["flair"] = from_str(self.flair)
        result["twitch_name"] = from_str(self.twitch_name)
        result["twitch_display_name"] = from_str(self.twitch_display_name)
        result["twitch_channel"] = from_str(self.twitch_channel)
        result["can_moderate"] = from_bool(self.can_moderate)
        result["stats"] = to_class(Stats, self.stats)
        return result


def user_from_dict(s: Any) -> User:
    return User.from_dict(s)


def user_to_dict(x: User) -> Any:
    return to_class(User, x)
