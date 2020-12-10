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
from models import *
from models.user import User

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
        if not isinstance(obj, dict):
            return None
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
        if not isinstance(obj, dict):
            return None
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
