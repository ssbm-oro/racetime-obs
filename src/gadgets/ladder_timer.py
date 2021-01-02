import asyncio
import logging
from datetime import datetime, timedelta
import pytz
from typing import List

from helpers import timer_to_str
import clients.ladder_client as ladder_client
from models.ladder import Flag, Racer, ScheduleItem, Season


class LadderTimer:
    logger: logging.Logger = None
    enabled: bool = False
    source_name = ""
    timer_text = ""
    racer_id: int = 0
    pre_color: int = 0xFFFFFF
    racing_color: int = 0xFFFFFF
    winner_color: int = 0xFF0000
    loser_color: int = 0x00FF00
    ff_color: int = 0x00FF00
    started_at: datetime = None
    next_race: ScheduleItem = None
    active_racers: List[Racer] = None
    current_season: Season = None
    flags: List[Flag] = []
    all_seasons: List[Season] = []
    schedule: List[ScheduleItem] = []
    last_timer_update: datetime = None

    @staticmethod
    def ladder_timezone():
        return pytz.timezone('US/Eastern')

    def __init__(self, logger: logging.Logger, racer_id: int = None):
        self.logger = logger
        if racer_id is not None:
            self.racer_id = racer_id
        self.update()

    def update(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.update_active_racers())
        loop.run_until_complete(self.update_flags())
        loop.run_until_complete(self.update_season())
        loop.run_until_complete(
            self.update_schedule(self.current_season.season_id))
        loop.run_until_complete(self.update_timer())

    def get_timer_text(self):
        current_timer = timedelta(seconds=0)
        color = self.pre_color
        now = datetime.now(self.ladder_timezone())
        if self.started_at is None:
            current_timer = now - self.next_race.StartTime
            if (abs(current_timer.total_seconds()) < 600.0):
                loop = asyncio.new_event_loop()
                loop.run_until_complete(self.update_timer())
                loop.close()
            color = self.pre_color
        else:
            current_timer = now - self.started_at
            if current_timer.total_seconds() > 0:
                color = self.racing_color
        return color, timer_to_str(current_timer)

    def update_settings(self, racer_name: str):
        if racer_name is None or racer_name == "":
            return False
        racer_id = self.get_racer_id(racer_name)
        if racer_id == 0:
            return False
        else:
            self.racer_id = racer_id
            return True

    def get_racer_id(self, racer_name: str) -> Racer:
        asyncio.wait(self.update_active_racers())
        for racer in self.active_racers:
            if racer.RacerName == racer_name:
                return racer.racer_id
        return 0

    async def update_active_racers(self):
        if self.active_racers is None or self.active_racers == []:
            self.active_racers = ladder_client.get_active_racers()

    async def update_season(self):
        if self.current_season is None:
            self.all_seasons = ladder_client.get_seasons()
            if self.all_seasons is not None:
                self.current_season = self.all_seasons[-1]
        self.logger.info(f"current_season = {self.current_season}")

    async def update_flags(self):
        self.flags = ladder_client.get_flags()

    async def update_schedule(self, season_id: int):
        if self.schedule is None or self.schedule == []:
            self.schedule = ladder_client.get_schedule(season_id)
            self.next_race = (
                next(x for x in self.schedule if not x.HasCompleted)
            )
            self.logger.info(f"next_race = {self.next_race}")

    async def update_timer(self):
        if (
            self.last_timer_update is not None and
            (datetime.now() - self.last_timer_update) < timedelta(seconds=20)
        ):
            return
        self.logger.debug("calling get_current_race_time to update timer")
        str_timer = ladder_client.get_current_race_time()
        self.last_timer_update = datetime.now()
        self.logger.info(f"str_timer= {str_timer}")
        timer_sign = 1.0
        if str_timer[0] == '-':
            timer_sign = -1.0
            str_timer = str_timer[1:]
        timer = timedelta(
            hours=float(str_timer[0:1]), minutes=float(str_timer[2:4]),
            seconds=float(str_timer[5:7]))
        timer = timer * timer_sign
        if timer == timedelta(seconds=0):
            self.started_at = None
        else:
            self.started_at = datetime.now(self.ladder_timezone()) - timer
