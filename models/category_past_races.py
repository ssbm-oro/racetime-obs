# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = category_past_races_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable
from enum import Enum
from datetime import datetime
import dateutil.parser
from models import *
from models.race import Race

@dataclass
class CategoryPastRaces:
    count: int
    num_pages: int
    races: List[Race]

    @staticmethod
    def from_dict(obj: Any) -> 'CategoryPastRaces':
        assert isinstance(obj, dict)
        count = from_int(obj.get("count"))
        num_pages = from_int(obj.get("num_pages"))
        races = from_list(Race.from_dict, obj.get("races"))
        return CategoryPastRaces(count, num_pages, races)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_int(self.count)
        result["num_pages"] = from_int(self.num_pages)
        result["races"] = from_list(lambda x: to_class(Race, x), self.races)
        return result


def category_past_races_from_dict(s: Any) -> CategoryPastRaces:
    return CategoryPastRaces.from_dict(s)


def category_past_races_to_dict(x: CategoryPastRaces) -> Any:
    return to_class(CategoryPastRaces, x)
