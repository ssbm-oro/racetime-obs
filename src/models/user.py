from dataclasses import dataclass
from typing import Any, Optional
from models import from_int, from_str, from_union, from_none, from_bool


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
        discriminator = from_union(
            [from_str, from_none], obj.get("discriminator"))
        url = from_str(obj.get("url"))
        avatar = from_union([from_str, from_none], obj.get("avatar"))
        pronouns = from_union([from_str, from_none], obj.get("pronouns"))
        flair = from_union([from_str, from_none], obj.get("flair"))
        twitch_name = from_union([from_str, from_none], obj.get("twitch_name"))
        twitch_display_name = from_union(
            [from_str, from_none], obj.get("twitch_display_name"))
        twitch_channel = from_union(
            [from_str, from_none], obj.get("twitch_channel"))
        can_moderate = from_union(
            [from_bool, from_none], obj.get("can_moderate"))
        stats = from_union([Stats.from_dict, from_none], obj.get("stats"))
        return User(id=id, full_name=full_name, name=name, discriminator=discriminator, url=url, avatar=avatar, pronouns=pronouns, flair=flair, twitch_name=twitch_name, twitch_display_name=twitch_display_name, twitch_channel=twitch_channel, can_moderate=can_moderate, stats=stats)


def user_from_dict(s: Any) -> User:
    return User.from_dict(s)
