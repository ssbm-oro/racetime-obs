# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = leaderboards_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable


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


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Flair(Enum):
    EMPTY = ""
    MODERATOR = "moderator"
    SUPPORTER = "supporter"
    SUPPORTER_MODERATOR = "supporter moderator"


class Pronouns(Enum):
    HE_HIM = "he/him"
    SHE_HER = "she/her"
    THEY_THEM = "they/them"


@dataclass
class User:
    id: str
    full_name: str
    name: str
    url: str
    flair: Flair
    can_moderate: bool
    discriminator: Optional[str] = None
    avatar: Optional[str] = None
    pronouns: Optional[Pronouns] = None
    twitch_name: Optional[str] = None
    twitch_display_name: Optional[str] = None
    twitch_channel: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        full_name = from_str(obj.get("full_name"))
        name = from_str(obj.get("name"))
        url = from_str(obj.get("url"))
        flair = Flair(obj.get("flair"))
        can_moderate = from_bool(obj.get("can_moderate"))
        discriminator = from_union([from_none, from_str], obj.get("discriminator"))
        avatar = from_union([from_none, from_str], obj.get("avatar"))
        pronouns = from_union([from_none, Pronouns], obj.get("pronouns"))
        twitch_name = from_union([from_none, from_str], obj.get("twitch_name"))
        twitch_display_name = from_union([from_none, from_str], obj.get("twitch_display_name"))
        twitch_channel = from_union([from_none, from_str], obj.get("twitch_channel"))
        return User(id, full_name, name, url, flair, can_moderate, discriminator, avatar, pronouns, twitch_name, twitch_display_name, twitch_channel)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["full_name"] = from_str(self.full_name)
        result["name"] = from_str(self.name)
        result["url"] = from_str(self.url)
        result["flair"] = to_enum(Flair, self.flair)
        result["can_moderate"] = from_bool(self.can_moderate)
        result["discriminator"] = from_union([from_none, from_str], self.discriminator)
        result["avatar"] = from_union([from_none, from_str], self.avatar)
        result["pronouns"] = from_union([from_none, lambda x: to_enum(Pronouns, x)], self.pronouns)
        result["twitch_name"] = from_union([from_none, from_str], self.twitch_name)
        result["twitch_display_name"] = from_union([from_none, from_str], self.twitch_display_name)
        result["twitch_channel"] = from_union([from_none, from_str], self.twitch_channel)
        return result


@dataclass
class Ranking:
    user: User
    place: int
    place_ordinal: str
    score: int
    best_time: str
    times_raced: int

    @staticmethod
    def from_dict(obj: Any) -> 'Ranking':
        assert isinstance(obj, dict)
        user = User.from_dict(obj.get("user"))
        place = from_int(obj.get("place"))
        place_ordinal = from_str(obj.get("place_ordinal"))
        score = from_int(obj.get("score"))
        best_time = from_str(obj.get("best_time"))
        times_raced = from_int(obj.get("times_raced"))
        return Ranking(user, place, place_ordinal, score, best_time, times_raced)

    def to_dict(self) -> dict:
        result: dict = {}
        result["user"] = to_class(User, self.user)
        result["place"] = from_int(self.place)
        result["place_ordinal"] = from_str(self.place_ordinal)
        result["score"] = from_int(self.score)
        result["best_time"] = from_str(self.best_time)
        result["times_raced"] = from_int(self.times_raced)
        return result


@dataclass
class Leaderboard:
    goal: str
    num_ranked: int
    rankings: List[Ranking]

    @staticmethod
    def from_dict(obj: Any) -> 'Leaderboard':
        assert isinstance(obj, dict)
        goal = from_str(obj.get("goal"))
        num_ranked = from_int(obj.get("num_ranked"))
        rankings = from_list(Ranking.from_dict, obj.get("rankings"))
        return Leaderboard(goal, num_ranked, rankings)

    def to_dict(self) -> dict:
        result: dict = {}
        result["goal"] = from_str(self.goal)
        result["num_ranked"] = from_int(self.num_ranked)
        result["rankings"] = from_list(lambda x: to_class(Ranking, x), self.rankings)
        return result


@dataclass
class Leaderboards:
    leaderboards: List[Leaderboard]

    @staticmethod
    def from_dict(obj: Any) -> 'Leaderboards':
        assert isinstance(obj, dict)
        leaderboards = from_list(Leaderboard.from_dict, obj.get("leaderboards"))
        return Leaderboards(leaderboards)

    def to_dict(self) -> dict:
        result: dict = {}
        result["leaderboards"] = from_list(lambda x: to_class(Leaderboard, x), self.leaderboards)
        return result


def leaderboards_from_dict(s: Any) -> Leaderboards:
    return Leaderboards.from_dict(s)


def leaderboards_to_dict(x: Leaderboards) -> Any:
    return to_class(Leaderboards, x)
