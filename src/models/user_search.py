from dataclasses import dataclass
from typing import Any, List
from models import from_list
from models.user import User


@dataclass
class UserSearch:
    results: List[User]

    @staticmethod
    def from_dict(obj: Any) -> 'UserSearch':
        if not isinstance(obj, dict):
            return None
        results = from_list(User.from_dict, obj.get("results"))
        return UserSearch(results)


def user_search_from_dict(s: Any) -> UserSearch:
    return UserSearch.from_dict(s)
