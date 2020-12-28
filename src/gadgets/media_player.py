import asyncio
from asyncio.locks import Lock
from datetime import datetime, timedelta
import logging
from threading import Timer
from typing import List, Optional
from asyncio import Event
from helpers import timer_to_str
from models.race import Entrant, Race
from models.chat_message import ChatMessage


class MediaTrigger:
    place: Optional[int] = None
    entrant_count_trigger: Optional[int] = None
    media_file_path: str = ""
    triggered: bool = False
    race_started_at: datetime = None

    def __init__(
        self, media_file_path: str, place_trigger: int = None,
        entrant_count_trigger: int = None
    ):
        self.media_file_path = media_file_path
        self.place = place_trigger
        self.entrant_count_trigger = entrant_count_trigger

    def check_trigger(self, race: Race, entrant: Entrant):
        if (
            self.triggered or self.media_file_path == "" or
            race is None or entrant is None
        ):
            return False
        else:
            if (
                self.check_finish_place_entrant_count(race, entrant) or
                self.check_finish_place(entrant)
            ):
                self.triggered = True
                return True
        return False

    def check_finish_place(self, entrant: Entrant):
        if (
            self.entrant_count_trigger is not None or entrant.user is None or
            entrant.place is None
        ):
            return False
        else:
            return (
                entrant.place <= self.place
            )

    def check_finish_place_entrant_count(self, race: Race, entrant: Entrant):
        if None in [
            self.entrant_count_trigger, entrant.user, entrant.place,
            race.entrants_count
        ]:
            return False
        else:
            return (
                entrant.place <= self.place and
                race.entrants_count <= self.entrant_count_trigger
            )


class ChatTrigger:
    media_file_path: str = ""
    highlight_trigger: bool = False
    bot_trigger: bool = False
    system_trigger: bool = False
    message_plain_trigger: str = ""
    trigger_once: bool = False
    triggered: bool = False

    def __init__(self, media_file_path, highlight, bot, system, message_plain):
        self.media_file_path = media_file_path
        self.highlight_trigger = highlight
        self.bot_trigger = bot
        self.system_trigger = system
        self.message_plain_trigger = message_plain

    def check_trigger(self, chat_message: ChatMessage):
        def trigger_on_bot(bot_trigger: bool, chat_message: ChatMessage):
            return bot_trigger and chat_message.is_bot

        def trigger_on_highlight(
                highlight_trigger: bool, chat_message: ChatMessage):
            return highlight_trigger and chat_message.highlight

        def trigger_on_system(system_trigger: bool, chat_message: ChatMessage):
            return system_trigger and chat_message.is_system

        if self.trigger_once and self.triggered:
            return False
        self.triggered = (
            trigger_on_bot(self.bot_trigger, chat_message) or
            trigger_on_highlight(self.highlight_trigger, chat_message) or
            trigger_on_system(self.system_trigger, chat_message)
        )
        return self.triggered


class MediaPlayer:
    logger: logging.Logger = logging.Logger("racetime-obs")
    enabled: bool = False
    triggers: List[MediaTrigger] = []
    chat_triggers: List[ChatTrigger] = []
    timers: List[Timer] = []
    triggers_lock: Lock = Lock()
    race_update_event: Event()
    play_media_callback = None
    started_at: datetime = None
    ping_chat_messages: bool = False
    chat_media_file: str = None
    last_session_race: str = ""
    monitoring_type: int = 0

    def race_updated(self, race: Race, entrant_name: str):
        # so the sound doesn't play when the user starts obs next time
        if self.last_session_race == race.name:
            return
        self.started_at = race.started_at
        for trigger in self.triggers:
            self.logger.debug(trigger)
            if trigger.check_trigger(
                race, race.get_entrant_by_name(entrant_name)
            ):
                self.play_media_callback(
                    trigger.media_file_path, self.monitoring_type)
                self.logger.debug("trigger fired")

    def chat_updated(self, message: ChatMessage):
        for trigger in self.chat_triggers:
            self.logger.debug(trigger)
            if trigger.check_trigger(message):
                self.play_media_callback(
                    trigger.media_file_path, self.monitoring_type)

    def add_trigger(
        self, media_file_path: str, place: int = None,
        entrant_count: int = None
    ):
        async def add(
            media_file_path: str, place_trigger: int = None,
            entrant_count_trigger: int = None
        ):
            async with self.triggers_lock:
                self.triggers.append(MediaTrigger(
                    media_file_path, place_trigger=place_trigger,
                    entrant_count_trigger=entrant_count_trigger
                ))

        asyncio.ensure_future(add(media_file_path, place, entrant_count))

    def add_chat_trigger(
            self, media_file_path: str, highlight: bool = False,
            is_bot: bool = False, is_system: bool = False,
            message_plain_text: str = None
            ):
        async def add(
            media_file_path, highlight, is_bot, is_system, message_plain_text
        ):
            async with self.triggers_lock:
                self.chat_triggers.append(
                    ChatTrigger(media_file_path, highlight, is_bot, is_system,
                                message_plain_text))
            pass
        asyncio.ensure_future(add(
            media_file_path, highlight, is_bot, is_system, message_plain_text))

    def add_timer(self, media_file_path: str, race_time: timedelta):
        # try to wake up a little early and get ready
        timer = Timer(
            self.time_to_start_play(race_time),
            self.timer_wake_up, media_file_path, race_time
        )
        self.timers.append(timer)
        timer.start()

    def time_to_start_play(self, race_time: timedelta) -> float:
        time_to_start_play = 10000000000000.0
        return time_to_start_play

    async def timer_wake_up(self, media_file_path: str, race_time: timedelta):
        asyncio.sleep(self.time_to_start_play(race_time))
        self.logger.debug(
            f"attempting to play {media_file_path} at "
            f"{timer_to_str(race_time)}"
        )
        asyncio.ensure_future(
            self.play_media_callback(
                media_file_path, self.monitoring_type))

    def remove_trigger(self, index: int):
        async def remove(index: int):
            async with self.triggers_lock:
                if len(self.triggers) > index:
                    self.triggers.remove(self.triggers[index])
        asyncio.ensure_future(remove(index))
