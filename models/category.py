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


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
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


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Flair(Enum):
    MODERATOR = "moderator"
    SUPPORTER_MODERATOR = "supporter moderator"


@dataclass
class Moderator:
    id: str
    full_name: str
    name: str
    discriminator: str
    url: str
    flair: Flair
    twitch_name: str
    twitch_display_name: str
    twitch_channel: str
    can_moderate: bool
    avatar: Optional[str] = None
    pronouns: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Moderator':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        full_name = from_str(obj.get("full_name"))
        name = from_str(obj.get("name"))
        discriminator = from_str(obj.get("discriminator"))
        url = from_str(obj.get("url"))
        flair = Flair(obj.get("flair"))
        twitch_name = from_str(obj.get("twitch_name"))
        twitch_display_name = from_str(obj.get("twitch_display_name"))
        twitch_channel = from_str(obj.get("twitch_channel"))
        can_moderate = from_bool(obj.get("can_moderate"))
        avatar = from_union([from_none, from_str], obj.get("avatar"))
        pronouns = from_union([from_none, from_str], obj.get("pronouns"))
        return Moderator(id, full_name, name, discriminator, url, flair, twitch_name, twitch_display_name, twitch_channel, can_moderate, avatar, pronouns)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["full_name"] = from_str(self.full_name)
        result["name"] = from_str(self.name)
        result["discriminator"] = from_str(self.discriminator)
        result["url"] = from_str(self.url)
        result["flair"] = to_enum(Flair, self.flair)
        result["twitch_name"] = from_str(self.twitch_name)
        result["twitch_display_name"] = from_str(self.twitch_display_name)
        result["twitch_channel"] = from_str(self.twitch_channel)
        result["can_moderate"] = from_bool(self.can_moderate)
        result["avatar"] = from_union([from_none, from_str], self.avatar)
        result["pronouns"] = from_union([from_none, from_str], self.pronouns)
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
    owners: List[Moderator]
    moderators: List[Moderator]
    goals: List[str]
    current_races: List[Any]

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
        owners = from_list(Moderator.from_dict, obj.get("owners"))
        moderators = from_list(Moderator.from_dict, obj.get("moderators"))
        goals = from_list(from_str, obj.get("goals"))
        current_races = from_list(lambda x: x, obj.get("current_races"))
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
        result["owners"] = from_list(lambda x: to_class(Moderator, x), self.owners)
        result["moderators"] = from_list(lambda x: to_class(Moderator, x), self.moderators)
        result["goals"] = from_list(from_str, self.goals)
        result["current_races"] = from_list(lambda x: x, self.current_races)
        return result


def category_from_dict(s: Any) -> Category:
    return Category.from_dict(s)


def category_to_dict(x: Category) -> Any:
    return to_class(Category, x)
