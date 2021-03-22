import asyncio
import logging
from datetime import datetime, timedelta
import pytz
from typing import List
from threading import Thread

from helpers import timer_to_str
import clients.ladder_client as ladder_client
from models.ladder import Flag, Racer, ScheduleItem, Season, Standings


def str_to_timer(str_timer):
    return timedelta(
        hours=float(str_timer[0:1]), minutes=float(str_timer[2:4]),
        seconds=float(str_timer[5:7]))


class LadderTimer:
    logger: logging.Logger = None
    enabled: bool = False
    source_name = ""
    timer_text = ""
    racer_id: int = 0
    racer_name: str = ""
    stats_source: str = ""
    stats: Standings = None
    season_for_stats: int = 0
    mode_for_stats: int = 0
    show_season_name: bool = False
    show_mode_name: bool = False
    show_rating: bool = False
    show_rank: bool = False
    show_change: bool = False
    show_win_loss_tie: bool = False
    pre_color: int = 0xFFFFFF
    racing_color: int = 0xFFFFFF
    winner_color: int = 0xFF0000
    loser_color: int = 0x00FF00
    ff_color: int = 0x00FF00
    started_at: datetime = None
    finish_time: timedelta = None
    result: str = ""
    next_race: ScheduleItem = None
    active_racers: List[Racer] = None
    current_season: Season = None
    flags: List[Flag] = []
    all_seasons: List[Season] = []
    schedule: List[ScheduleItem] = []
    last_timer_update: datetime = None
    decimals: bool = True

    @staticmethod
    def ladder_timezone():
        return pytz.timezone('US/Eastern')

    def __init__(self, logger: logging.Logger, racer_id: int = None):
        self.logger = logger
        if racer_id is not None:
            self.racer_id = racer_id

        ladder_update_t = Thread(target=self.ladder_update_thread)
        ladder_update_t.daemon = True
        ladder_update_t.start()

    def ladder_update_thread(self):
        self.logger.debug("starting ladder race update")
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.race_updater())
        loop.run_forever()

    async def race_updater(self):
        await self.update_active_racers()
        await self.update_flags()
        await self.update_season()
        await self.update_schedule(self.current_season.season_id)
        await self.update_timer()
        await self.update_stats()
        while True:
            if not self.enabled or self.finish_time is not None:
                await asyncio.sleep(5.0)
            else:
                now = datetime.now(self.ladder_timezone())
                if self.started_at is not None and now > self.started_at:
                    self.logger.debug("checking if racer finished")
                    await self.check_racer_finish()
                await asyncio.sleep(5.0)

    async def check_racer_finish(self):
        racer_history = ladder_client.get_racer_history(self.racer_id)
        if racer_history[-1].race_id == self.next_race.race_id:
            if racer_history[-1].FinishTime == "FF":
                self.result = "FF"
                self.finish_time = timedelta(seconds=0)
                self.logger.debug("racer forfeited")
            else:
                self.finish_time = str_to_timer(racer_history[-1].FinishTime)
                self.result = racer_history[-1].Result

    def get_timer_text(self):
        if self.finish_time:
            if self.result == "W":
                return (
                    self.winner_color,
                    timer_to_str(self.finish_time, self.decimals)
                )
            elif self.result == "L":
                return (
                    self.loser_color,
                    timer_to_str(self.finish_time, self.decimals)
                )
            elif self.result == "FF":
                return self.ff_color, "-:--:--.-"
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
        return color, timer_to_str(current_timer, self.decimals)

    def get_stats(self):
        stats = ""
        if self.enabled:
            if self.show_season_name:
                stats = stats + self.stats.Season + " "
            if self.show_mode_name:
                stats = stats + self.stats.Mode + " "
            if self.show_rank:
                stats = stats + "#" + str(self.stats.Rank) + " "
            if self.show_rating:
                stats = stats + str(self.stats.Rating) + " "
            if self.show_change:
                stats = stats + str(self.stats.Change) + " "
            if self.show_win_loss_tie:
                stats = (
                    stats + str(self.stats.Wins) + "/" +
                    str(self.stats.Losses) + "/" + str(self.stats.Ties)
                )
        return stats

    def update_settings(self, racer_name: str):
        if racer_name is None or racer_name == "":
            return False
        racer_id = self.get_racer_id(racer_name)
        if racer_id == 0:
            return False
        else:
            self.racer_id = racer_id
            self.racer_name = racer_name
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.update_stats())
            loop.close()
            return True

    def get_racer_id(self, racer_name: str) -> Racer:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.update_active_racers())
        loop.close()
        for racer in self.active_racers:
            if racer.RacerName.lower() == racer_name.lower():
                return racer.racer_id
        return 0

    async def update_active_racers(self):
        if self.active_racers is None or self.active_racers == []:
            self.active_racers = ladder_client.get_active_racers()

    async def update_season(self):
        if self.current_season is None:
            self.all_seasons = ladder_client.get_seasons()
            if self.all_seasons is not None:
                self.current_season = (
                    next(filter(
                        lambda x: x.IsCurrentSeason, self.all_seasons
                    ), None)
                )
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
        self.logger.debug("calling get_current_race_time")
        str_timer = ladder_client.get_current_race_time()
        self.last_timer_update = datetime.now()
        self.logger.info(f"str_timer= {str_timer}")
        timer_sign = 1.0
        if str_timer[0] == '-':
            timer_sign = -1.0
            str_timer = str_timer[1:]
        timer = str_to_timer(str_timer)
        timer = timer * timer_sign
        if timer == timedelta(seconds=0):
            self.started_at = None
        else:
            self.started_at = datetime.now(self.ladder_timezone()) - timer

    async def update_stats(self):
        if self.season_for_stats == -1:
            self.season_for_stats = self.current_season.season_id
        if self.mode_for_stats == -1:
            self.mode_for_stats = self.get_mode_id_from_name(
                self.next_race.Mode)
        self.logger.info(f"season_for_stats: {self.season_for_stats}")
        self.logger.info(f"mode_for_stats: {self.mode_for_stats}")
        standings = ladder_client.get_standings(
            self.season_for_stats, self.mode_for_stats)
        for stats in standings:
            if stats.RacerName.lower() == self.racer_name.lower():
                self.stats = stats
                return
        # default standings
        self.stats = Standings(
            self.racer_name, self.current_season.SeasonName,
            self.next_race.Mode, 1600, 0, 0, 0, 0, 0)

    def get_mode_id_from_name(self, mode_name: str):
        for flag in self.flags:
            if flag.Mode == mode_name:
                return flag.flag_id
