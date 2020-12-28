import asyncio
import logging
from datetime import timedelta
from typing import List

from helpers import timer_to_str
import clients.ladder_client as ladder_client
from models.ladder import Flag, Racer, ScheduleItem, Season


class LadderTimer:
    logger: logging.Logger = None
    enabled: bool = False
    source_name = ""
    timer_text = ""
    racer_id: int
    pre_color: int
    racing_color: int
    winner_color: int
    loser_color: int
    ff_color: int
    timer: timedelta
    next_race: ScheduleItem
    active_racers: List[Racer]
    current_season: Season
    flags: List[Flag]
    schedule: List[ScheduleItem]

    def __init__(self, racer_id=None):
        updates = asyncio.gather(
            self.update_active_racers, self.update_season, self.update_flags,
            self.update_schedule)
        asyncio.ensure_future(updates)
        if racer_id is not None:
            self.racer_id = racer_id

    def get_timer_text(self):
        return self.racing_color, timer_to_str(self.timer)

    def update_settings(self, racer_name: str):
        racer_id = self.get_racer_id(racer_name)
        if racer_id == 0:
            return False
        else:
            self.racer_id = racer_id
            return True

    def get_racer_id(self, racer_name: str) -> Racer:
        self.update_active_racers()
        for racer in self.active_racers:
            if racer.RacerName == racer_name:
                return racer.racer_id
        return 0

    async def update_active_racers(self):
        if self.active_racers is None or self.active_racers == []:
            self.active_racers = ladder_client.get_active_racers()

    async def update_season(self) -> List[Season]:
        if self.season is None:
            seasons = ladder_client.get_seasons()
            if seasons is not None:
                self.season = seasons[-1]

    async def update_flags(self) -> List[Flag]:
        if self.flags is None or self.seasons == []:
            self.flags = ladder_client.get_flags()

    async def update_schedule(self) -> List[ScheduleItem]:
        if self.schedule is None or self.schedule == []:
            self.schedule = ladder_client.get_schedule()
            self.next_race = (
                next(x for x in self.schedule if not x.HasCompleted)
            )
