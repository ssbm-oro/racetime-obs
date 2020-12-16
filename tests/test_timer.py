from datetime import datetime, timedelta, timezone
from gadgets.timer import Timer
from models.race import Entrant, Goal, Race, Status
from users_for_testing import get_test_user
from categories_for_testing import get_test_race_category


def get_test_entrant(status_value="joined", finished_at: datetime = None, finish_time: timedelta = None) -> Entrant:
    return Entrant(get_test_user(), status=get_test_status(status_value), has_comment=False, stream_live=True, stream_override=False, actions=[], finished_at=finished_at, finish_time=finish_time)

def get_test_status(status_value):
    Status(value=status_value, verbose_value="", help_text="")

def get_test_race(status_value="in_progress", version=1, entrants_count=2, started_at=datetime.now(timezone.utc), start_delay=timedelta(seconds=-15), 
                opened_at=datetime.now(timezone.utc), ended_at=None, cancelled_at: datetime = None, entrant: Entrant = None) -> Race:
    test_race= Race(name="",
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
                entrants_count_finished=0,
                entrants=(list(get_test_entrant()
                          for x in range(0, entrants_count))),
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

def get_test_timer():
    timer = Timer()
    timer.source_name = "Timer source"
    timer.enabled = True
    return timer


def test_timer_prerace():
    timer = get_test_timer()
    race = get_test_race(status_value="open", version=12,
                         started_at=None, start_delay=timedelta(seconds=-15))
    color, text = timer.get_timer_text(race, "")
    assert color is None
    assert text == "-0:00:15.0"

    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, "")
    assert color is timer.pre_color
    assert text == "-0:00:15.0"

def test_timer_midrace():
    timer = get_test_timer()
    race1 = get_test_race(status_value="in_progress", version=15, entrants_count=2,
        started_at=datetime.now(timezone.utc)-timedelta(hours=1, minutes=20))
    color, text = timer.get_timer_text(race1, "")
    assert color is None
    # hope this always runs in less than 0.1 seconds XD
    assert text == "1:20:00.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race1, "")
    assert color is timer.racing_color

    timer.use_podium_colors = False
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, minutes=42, seconds=6.9))
    race2 = get_test_race(version=16, entrants_count=2, entrant=entrant)
    color, text = timer.get_timer_text(race2, entrant.user.full_name)
    assert color is None
    assert text == "1:42:06.9"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race2, entrant.user.full_name)
    assert color == timer.racing_color

    timer.use_podium_colors = False
    race3 = get_test_race(version=17, entrants_count=2, started_at=datetime.now(timezone.utc)-timedelta(hours=1, minutes=42, seconds=42.0))
    color, text = timer.get_timer_text(race3, "user_not_in_race#6969")
    assert color is None
    assert text == "1:42:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race3, "user_not_in_race#6969")
    assert color == timer.racing_color

    

    