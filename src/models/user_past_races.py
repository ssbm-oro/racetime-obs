from dataclasses import dataclass
from typing import Any, List
from models import from_int, from_list
from models.race import Race

@dataclass
class UserPastRaces:
    count: int
    num_pages: int
    races: List[Race]

    @staticmethod
    def from_dict(obj: Any) -> 'UserPastRaces':
        if not isinstance(obj, dict):
            return None
        count = from_int(obj.get("count"))
        num_pages = from_int(obj.get("num_pages"))
        races = from_list(Race.from_dict, obj.get("races"))
        return UserPastRaces(count, num_pages, races)


def user_past_races_from_dict(s: Any) -> UserPastRaces:
    return UserPastRaces.from_dict(s)
