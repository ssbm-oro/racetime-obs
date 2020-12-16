from dataclasses import dataclass
from typing import Any, List
from models import from_int, from_str, from_list
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


@dataclass
class Leaderboards:
    leaderboards: List[Leaderboard]

    @staticmethod
    def from_dict(obj: Any) -> 'Leaderboards':
        assert isinstance(obj, dict)
        leaderboards = from_list(Leaderboard.from_dict, obj.get("leaderboards"))
        return Leaderboards(leaderboards)


def leaderboards_from_dict(s: Any) -> Leaderboards:
    return Leaderboards.from_dict(s)
