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
#     result = user_past_races_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable
from datetime import datetime, timedelta
import dateutil.parser
from models import *
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

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_int(self.count)
        result["num_pages"] = from_int(self.num_pages)
        result["races"] = from_list(lambda x: to_class(Race, x), self.races)
        return result


def user_past_races_from_dict(s: Any) -> UserPastRaces:
    return UserPastRaces.from_dict(s)


def user_past_races_to_dict(x: UserPastRaces) -> Any:
    return to_class(UserPastRaces, x)
