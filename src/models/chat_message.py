from dataclasses import dataclass
from typing import Any
from datetime import datetime
from models import (
    from_str, from_bool, from_datetime
)
from models.user import User, user_from_dict


@dataclass
class ChatMessage:
    id: str
    user: User
    bot: str
    posted_at: datetime
    message: str
    message_plain: str
    highlight: bool
    is_bot: bool
    is_system: bool

    @staticmethod
    def from_dict(obj: Any) -> 'ChatMessage':
        if not isinstance(obj, dict):
            return None
        id = from_str(obj.get("id"))
        user = user_from_dict(obj.get("user"))
        bot = from_str(obj.get("bot"))
        posted_at = from_datetime(obj.get("posted_at"))
        message = from_str(obj.get("message"))
        message_plain = from_str(obj.get("message_plain"))
        highlight = from_bool(obj.get("highlight"))
        is_bot = from_bool(obj.get("is_bot"))
        is_system = from_bool(obj.get("is_system"))

        return ChatMessage(
            id=id, user=user, bot=bot, posted_at=posted_at, message=message,
            message_plain=message_plain, highlight=highlight, is_bot=is_bot,
            is_system=is_system)


def chat_message_from_dict(s: Any) -> ChatMessage:
    return ChatMessage.from_dict(s)
