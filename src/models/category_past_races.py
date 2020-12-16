from dataclasses import dataclass
from typing import Any, List
from models import from_int, from_list
from models.race import Race

@dataclass
class CategoryPastRaces:
    count: int
    num_pages: int
    races: List[Race]

    @staticmethod
    def from_dict(obj: Any) -> 'CategoryPastRaces':
        if not isinstance(obj, dict):
            return None
        count = from_int(obj.get("count"))
        num_pages = from_int(obj.get("num_pages"))
        races = from_list(Race.from_dict, obj.get("races"))
        return CategoryPastRaces(count, num_pages, races)


def category_past_races_from_dict(s: Any) -> CategoryPastRaces:
    return CategoryPastRaces.from_dict(s)
