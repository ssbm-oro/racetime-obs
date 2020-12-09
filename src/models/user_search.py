# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = user_search_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Any, List, TypeVar, Callable, Type, cast
from models import *
from models.user import User


@dataclass
class UserSearch:
    results: List[User]

    @staticmethod
    def from_dict(obj: Any) -> 'UserSearch':
        assert isinstance(obj, dict)
        results = from_list(User.from_dict, obj.get("results"))
        return UserSearch(results)

    def to_dict(self) -> dict:
        result: dict = {}
        result["results"] = from_list(lambda x: to_class(User, x), self.results)
        return result


def user_search_from_dict(s: Any) -> UserSearch:
    return UserSearch.from_dict(s)


def user_search_to_dict(x: UserSearch) -> Any:
    return to_class(UserSearch, x)
