# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = user_search_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Result:
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

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
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
        return Result(id, full_name, name, discriminator, url, avatar, pronouns, flair, twitch_name, twitch_display_name, twitch_channel, can_moderate)

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
        return result


@dataclass
class UserSearch:
    results: List[Result]

    @staticmethod
    def from_dict(obj: Any) -> 'UserSearch':
        assert isinstance(obj, dict)
        results = from_list(Result.from_dict, obj.get("results"))
        return UserSearch(results)

    def to_dict(self) -> dict:
        result: dict = {}
        result["results"] = from_list(lambda x: to_class(Result, x), self.results)
        return result


def user_search_from_dict(s: Any) -> UserSearch:
    return UserSearch.from_dict(s)


def user_search_to_dict(x: UserSearch) -> Any:
    return to_class(UserSearch, x)
