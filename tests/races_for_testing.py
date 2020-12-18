from datetime import datetime, timedelta, timezone
from typing import List

from models.race import Entrant, Goal, Race, Status

from categories_for_testing import get_test_race_category
from users_for_testing import get_test_entrant, get_test_user


def time_ago(**kwargs):
    return datetime.now(timezone.utc)-timedelta(**kwargs)


def get_test_race(status_value="in_progress", version=1, entrants_count=2, started_at=datetime.now(timezone.utc),
                  start_delay=timedelta(seconds=-15), opened_at=datetime.now(timezone.utc), ended_at=None,
                  cancelled_at: datetime = None, entrant: Entrant = None, entrants: List[Entrant] = None) -> Race:
    if not entrants:
        entrants = []
        for i in range(0, entrants_count):
            e = get_test_entrant(entrants)
            entrants.append(e)
        entrant_count_finished = 0
    else:
        entrant_count_finished = list.count(
            (list((x.status.value == "finished" for x in entrants))), True)
    test_race = Race(name="",
                     status=Status(value=status_value,
                                   verbose_value="", help_text=""),
                     category=get_test_race_category(),
                     goal=Goal("", False),
                     info="A test race",
                     url="",
                     data_url="",
                     websocket_url="",
                     websocket_bot_url="",
                     websocket_oauth_url="",
                     entrants_count=entrants_count,
                     entrants_count_inactive=0,
                     entrants_count_finished=entrant_count_finished,
                     entrants=entrants,
                     version=version,
                     started_at=started_at,
                     start_delay=start_delay,
                     ended_at=ended_at,
                     cancelled_at=cancelled_at,
                     unlisted=False,
                     time_limit=timedelta(days=1),
                     streaming_required=True,
                     auto_start=True,
                     opened_by=get_test_user(),
                     opened_at=opened_at,
                     monitors=[],
                     recordable=True,
                     recorded=False,
                     recorded_by=None,
                     allow_comments=True,
                     hide_comments=False,
                     allow_midrace_chat=True
                     )
    if entrant is not None:
        if not entrant in test_race.entrants:
            test_race.entrants.pop()
            test_race.entrants.append(entrant)
    return test_race
