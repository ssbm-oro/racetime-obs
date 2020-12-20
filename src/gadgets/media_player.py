import asyncio
from asyncio.events import AbstractEventLoop
from asyncio.locks import Lock
from datetime import datetime, timedelta  # , timezone
import logging
from threading import Timer
from typing import List, Optional
from asyncio import Condition, Event
from models.race import Entrant, Race
from gadgets.timer import Timer as GadgetTimer


class MediaConditionTrigger:
    place: Optional[int] = None
    entrant_count_trigger: Optional[int] = None
    media_file_path: str = ""
    triggered: bool = False
    race_started_at: datetime = None
    race_update_condition: Condition = Condition()

    def __init__(
        self, media_file_path: str, place_trigger: int = None,
        entrant_count_trigger: int = None
    ):
        self.media_file_path = media_file_path
        self.place = place_trigger
        self.entrant_count_trigger = entrant_count_trigger

    def check_trigger(self, race: Race, entrant: Entrant):
        if self.triggered or self.media_file_path == "":
            return False
        else:
            if (
                self.check_finish_place_entrant_count(race, entrant) or
                self.check_finish_place(race, entrant)
            ):
                self.triggered = True
                return True
        return False

    def check_finish_place(self, race: Race, entrant: Entrant):
        if (
            self.entrant_count_trigger is None and race is not None and
            entrant is not None and entrant.user is not None
        ):
            user = race.get_entrant_by_name(entrant.user.full_name)
            return (
                user.place <= self.place
            )

    def check_finish_place_entrant_count(self, race: Race, entrant: Entrant):
        if (
            self.entrant_count_trigger is not None and race is not None and
            entrant is not None and entrant.user is not None
        ):
            user = race.get_entrant_by_name(entrant.user.full_name)
            return (
                user.place <= self.place and
                race.entrants_count <= self.entrant_count_trigger
            )


class MediaPlayer:
    logger: logging.Logger = logging.Logger("racetime-obs")
    entrant_name: str = ""
    enabled: bool = False
    triggers: List[MediaConditionTrigger] = []
    timers: List[Timer] = []
    triggers_lock: Lock = Lock()
    race_update_event: Event()
    play_media_callback = None
    event_loop: AbstractEventLoop = None
    started_at: datetime = None
    ping_chat_messages: bool = False
    chat_media_file: str = None

    def __init__(self, event_loop: AbstractEventLoop):
        self.event_loop = event_loop

    def race_updated(self, race: Race):
        self.started_at = race.started_at
        for trigger in self.triggers:
            if trigger.check_trigger(
                race, race.get_entrant_by_name(self.entrant_name)
            ):
                self.play_media_callback(trigger.media_file_path, True)
                self.logger.debug("trigger fired")

    def add_trigger(
        self, media_file_path: str, place_trigger: int = None,
        entrant_count_trigger: int = None
    ):
        async def add(
            self, media_file_path: str, place_trigger: int = None,
            entrant_count_trigger: int = None
        ):
            async with self.triggers_lock:
                self.triggers.append(MediaConditionTrigger(
                    media_file_path, place_trigger=place_trigger,
                    entrant_count_trigger=entrant_count_trigger
                ))

        self.event_loop.run_until_complete(
            add(
                media_file_path, place_trigger,
                entrant_count_trigger
            )
        )

    def add_timer(self, media_file_path: str, race_time: timedelta):
        # try to wake up a little early and get ready
        timer = Timer(
            self.time_to_start_play(race_time),
            self.timer_wake_up, media_file_path, race_time
        )
        self.timers.append(timer)
        timer.start()

    def time_to_start_play(self, race_time: timedelta) -> float:
        # time_to_start_play = (
        #     race_time - datetime.now(timezone.utc) -
        #     self.started_at - timedelta(seconds=1.0)
        # )
        time_to_start_play = 10000000000000.0
        return time_to_start_play

    async def timer_wake_up(self, media_file_path: str, race_time: timedelta):
        asyncio.sleep(self.time_to_start_play(race_time))
        self.logger.debug(
            f"attempting to play {media_file_path} at "
            f"{GadgetTimer.timer_to_str(race_time)}"
        )
        self.event_loop.call_soon_threadsafe(
            self.play_media_callback, media_file_path, True
        )

    def remove_trigger(self, index: int):
        async def remove(index: int):
            async with self.triggers_lock:
                self.triggers.clear()

        self.event_loop.run_until_complete(remove(index))
