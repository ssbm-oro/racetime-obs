from dataclasses import dataclass
from datetime import datetime
from typing import Any, List

import pytz
from models import (
    from_bool, from_datetime, from_int, from_list, from_none, from_str,
    from_union
)


@dataclass
class Racer:
    racer_id: int
    RacerName: str

    @staticmethod
    def from_dict(obj: Any) -> 'Racer':
        if not isinstance(obj, dict):
            return None
        racer_id = from_int(obj.get("racer_id"))
        RacerName = from_str(obj.get("RacerName"))
        return Racer(racer_id=racer_id, RacerName=RacerName)


def racers_from_dict(s: Any) -> List[Racer]:
    assert isinstance(s, List)
    if not s:
        return []
    return from_union(
        [lambda x: from_list(Racer.from_dict, x), from_none], s
    )


@dataclass
class Flag:
    Mode: str
    flag_id: int
    HoursToComplete: int

    @staticmethod
    def from_dict(obj: Any) -> 'Flag':
        if not isinstance(obj, dict):
            return None
        Mode = from_str(obj.get("Mode"))
        flag_id = from_int(obj.get("flag_id"))
        HoursToComplete = from_int(obj.get("HoursToComplete"))
        return Flag(
            Mode=Mode, flag_id=flag_id, HoursToComplete=HoursToComplete)


def flags_from_dict(s: Any) -> List[Flag]:
    assert isinstance(s, List)
    if not s:
        return []
    return from_union(
        [lambda x: from_list(Flag.from_dict, x), from_none], s
    )


@dataclass
class Season:
    season_id: int
    SeasonName: str

    @staticmethod
    def from_dict(obj: Any) -> 'Season':
        if not isinstance(obj, dict):
            return None
        season_id = from_int(obj.get("season_id"))
        SeasonName = from_str(obj.get("SeasonName"))
        return Season(season_id=season_id, SeasonName=SeasonName)


def seasons_from_dict(s: Any) -> List[Season]:
    assert isinstance(s, List)
    if not s:
        return []
    return from_union(
        [lambda x: from_list(Season.from_dict, x), from_none], s
    )


@dataclass
class Standings:
    RacerName: str
    Season: str
    Mode: str
    Rating: int
    Rank: int
    Change: int
    Wins: int
    Losses: int
    Ties: int

    @staticmethod
    def from_dict(obj: Any) -> 'Standings':
        if not isinstance(obj, dict):
            return None
        RacerName = from_str(obj.get("RacerName"))
        Season = from_str(obj.get("Season"))
        Mode = from_str(obj.get("Mode"))
        Rating = from_int(obj.get("Rating"))
        Rank = from_int(obj.get("Rank"))
        Change = from_int(obj.get("Change"))
        Wins = from_int(obj.get("Wins"))
        Losses = from_int(obj.get("Losess"))
        Ties = from_int(obj.get("Ties"))
        return Standings(
            RacerName=RacerName, Season=Season, Mode=Mode, Rating=Rating,
            Rank=Rank, Change=Change, Wins=Wins, Losses=Losses, Ties=Ties)


def standings_from_dict(s: Any) -> List[Standings]:
    assert isinstance(s, List)
    if not s:
        return []
    return from_union(
        [lambda x: from_list(Standings.from_dict, x), from_none], s
    )


@dataclass
class RacerResult:
    RacerName: str
    OpponentRacerName: str
    Mode: str
    Season: str
    Result: str
    FinishTime: str
    OpponentFinishTime: str

    def from_dict(obj: Any) -> 'RacerResult':
        if not isinstance(obj, dict):
            return None
        RacerName = from_str(obj.get("RacerName"))
        OpponentRacerName = from_str(obj.get("OpponentRacerName"))
        Mode = from_str(obj.get("Mode"))
        Season = from_str(obj.get("Season"))
        Result = from_str(obj.get("Result"))
        FinishTime = from_str(obj.get("FinishTime"))
        OpponentFinishTime = from_str(obj.get("OpponentFinishTime"))
        return RacerResult(
            RacerName=RacerName, OpponentRacerName=OpponentRacerName,
            Mode=Mode, Season=Season, Result=Result, FinishTime=FinishTime,
            OpponentFinishTime=OpponentFinishTime
        )


def racer_results_from_dict(s: Any) -> List[RacerResult]:
    assert isinstance(s, List)
    if not s:
        return []
    return from_union(
        [lambda x: from_list(RacerResult.from_dict, x), from_none], s
    )


@dataclass
class ScheduleItem:
    Season: str
    Mode: str
    StartTime: datetime
    RaceName: str
    HasCompleted: bool
    ParticipantCount: int

    @staticmethod
    def from_dict(obj: Any) -> 'Standings':
        if not isinstance(obj, dict):
            return None
        Season = from_str(obj.get("Season"))
        Mode = from_str(obj.get("Mode"))
        StartTime = (pytz.timezone('US/Eastern').localize(
                from_datetime(obj.get("StartTime"))
            ))
        RaceName = from_str(obj.get("RaceName"))
        HasCompleted = from_bool(obj.get("HasCompleted"))
        ParticipantCount = from_int(obj.get("ParticipantCount"))
        return ScheduleItem(
            Season=Season, Mode=Mode, StartTime=StartTime, RaceName=RaceName,
            HasCompleted=HasCompleted, ParticipantCount=ParticipantCount
        )


def schedule_from_dict(s: Any) -> List[ScheduleItem]:
    assert isinstance(s, List)
    if not s:
        return []
    return from_union(
        [lambda x: from_list(ScheduleItem.from_dict, x), from_none], s
    )
