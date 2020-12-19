from asyncio.locks import Lock
from datetime import timedelta, timezone, datetime
import logging
import asyncio
from threading import Thread
from typing import List, Optional
from asyncio import Condition, Event
from models.race import Entrant, Race
from rtgg_obs import RacetimeObs


class MediaTrigger:
    place: Optional[int] = None
    entrant_count_trigger: Optional[int] = None
    trigger_time: Optional[timedelta] = None
    media_file_path: str = ""
    triggered: bool = False
    race_started_at: datetime = None
    race_update_condition: Condition = Condition()
    timer_event: Event = Event()

    def __init__(
        self, media_file_path: str, place_trigger: int = None,
        entrant_count_trigger: int = None, trigger_time: timedelta = None
    ):
        self.media_file_path = media_file_path
        self.place = place_trigger
        self.entrant_count_trigger = entrant_count_trigger
        self.trigger_time = trigger_time

    def check_trigger(self, race: Race, entrant: Entrant):
        if self.triggered or self.media_file_path == "":
            return False
        else:
            current_time = datetime.now(timezone.utc) - race.started_at
            if (
                self.check_finish_place_entrant_count(race, entrant) or
                self.check_finish_place(race, entrant) or
                self.check_time(current_time, race, entrant)
            ):
                self.triggered = True
                return True
        return False

    async def timer_trigger(self, full_name):
        while self.race_started_at is None:
            await self.race_update_condition.wait(2.0)
        if self.trigger_time is not None:
            time_to_trigger = (
                self.race_started_at +
                self.trigger_time - timedelta(seconds=0.1)
            )
            time_until_trigger = time_to_trigger - datetime.now(timezone.utc)
            await asyncio.sleep(time_until_trigger)

    def check_time(
        self, current_time: timedelta, race: Race, entrant: Entrant
    ):
        if self.trigger_time is not None:
            return (
                current_time >= self.trigger_time and
                race.status.value != "finished" and
                entrant.status.value != "finished"
            )
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


class MediaTimerTrigger(MediaTrigger):
    def __init__(self, media_file_path: str, trigger_time: timedelta = None):
        self.media_file_path = media_file_path
        self.trigger_time = trigger_time

    async def start(self, timer_callback):
        loop = asyncio.get_event_loop()
        time_to_trigger = (
            self.race_started_at + self.trigger_time - timedelta(seconds=0.1)
        )
        loop.call_at(time_to_trigger.timestamp(), timer_callback)


class MediaPlayer:
    logger: logging.Logger = logging.Logger("racetime-obs")
    race: Race = None
    entrant: Entrant = None
    enabled: bool = False
    triggers: List[MediaTrigger] = []
    triggers_lock: Lock = Lock()
    race_update_event: Event()
    play_media_callback = None
    rtgg_obs: RacetimeObs = None

    def __init__(self, rtgg_obs: RacetimeObs):
        self.rtgg_obs = rtgg_obs
        race_monitor_t = Thread(target=self.race_monitor_thread)
        race_monitor_t.daemon = True
        race_monitor_t.start()

    def race_monitor_thread(self):
        self.logger.debug("starting race media_player thread")
        media_event_loop = asyncio.new_event_loop()
        media_event_loop.run_until_complete(self.monitor_race())
        media_event_loop.run_forever()

    def update_race(self, race: Race):
        self.race = race

        self.race_update_event.set()

    def add_trigger(
        self, media_file_path: str, place_trigger: int = None,
        entrant_count_trigger: int = None, trigger_time: timedelta = None
    ):
        media_event_loop = asyncio.get_event_loop()
        media_event_loop.run_until_complete(
            self._add_trigger(
                media_file_path, place_trigger,
                entrant_count_trigger, trigger_time
            )
        )

    async def _add_trigger(
        self, media_file_path: str, place_trigger: int = None,
        entrant_count_trigger: int = None, trigger_time: timedelta = None
    ):
        async with self.triggers_lock:
            self.triggers.append(MediaTrigger(
                media_file_path, place_trigger=place_trigger,
                entrant_count_trigger=entrant_count_trigger,
                trigger_time=trigger_time
            ))

    def remove_trigger(self, index: int):
        media_event_loop = asyncio.get_event_loop()
        media_event_loop.run_until_complete(
            self._remove_trigger(index)
        )

    async def _remove_trigger(self, index: int):
        async with self.triggers_lock:
            self.triggers.clear()
            # self.triggers.remove(self.triggers[index])

    async def monitor_race(self):
        while True:
            if(
                not self.enabled or self.race is None or
                self.play_media_callback is None
            ):
                await asyncio.sleep(5.0)
            else:
                await asyncio.sleep(0.1)
                async with self.triggers_lock:
                    for trigger in self.triggers:
                        if trigger.check_trigger(self.race, self.entrant):
                            loop = asyncio.get_event_loop()
                            loop.call_soon_threadsafe(
                                self.play_media_callback,
                                trigger.media_file_path
                            )
                            self.logger.debug("trigger fired")
