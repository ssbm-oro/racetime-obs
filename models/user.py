# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = user_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


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
        assert isinstance(obj, dict)
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
    discriminator: int
    url: str
    avatar: str
    pronouns: str
    flair: str
    twitch_name: str
    twitch_display_name: str
    twitch_channel: str
    can_moderate: bool
    stats: Stats

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        full_name = from_str(obj.get("full_name"))
        name = from_str(obj.get("name"))
        discriminator = int(from_str(obj.get("discriminator")))
        url = from_str(obj.get("url"))
        avatar = from_str(obj.get("avatar"))
        pronouns = from_str(obj.get("pronouns"))
        flair = from_str(obj.get("flair"))
        twitch_name = from_str(obj.get("twitch_name"))
        twitch_display_name = from_str(obj.get("twitch_display_name"))
        twitch_channel = from_str(obj.get("twitch_channel"))
        can_moderate = from_bool(obj.get("can_moderate"))
        stats = Stats.from_dict(obj.get("stats"))
        return User(id, full_name, name, discriminator, url, avatar, pronouns, flair, twitch_name, twitch_display_name, twitch_channel, can_moderate, stats)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["full_name"] = from_str(self.full_name)
        result["name"] = from_str(self.name)
        result["discriminator"] = from_str(str(self.discriminator))
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
