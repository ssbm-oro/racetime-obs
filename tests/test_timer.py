from datetime import datetime, time, timedelta, timezone
from races_for_testing import time_ago
from gadgets.timer import Timer
from models.race import Entrant, Goal, Race, Status
from users_for_testing import get_test_user, get_test_entrant
from categories_for_testing import get_test_race_category
from races_for_testing import get_test_race


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

def test_timer_counting_down():
    timer = get_test_timer()
    race = get_test_race(status_value="pending", version=13, started_at=time_ago(seconds=-5), start_delay=timedelta(seconds=-15))
    color, text = timer.get_timer_text(race, "")
    assert color is None
    assert text == "-0:00:05.0"
    
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, "")
    assert color is timer.pre_color

def test_timer_midrace_no_entrant():
    timer = get_test_timer()
    race = get_test_race(status_value="in_progress", version=15, entrants_count=2,
        started_at=datetime.now(timezone.utc)-timedelta(hours=1, minutes=20))
    color, text = timer.get_timer_text(race, "")
    assert color is None
    # hope this always runs in less than 0.1 seconds XD
    assert text == "1:20:00.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, "")
    assert color is timer.racing_color


def test_timer_midrace_w_entrant():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, minutes=42, seconds=6.9))
    race = get_test_race(version=16, entrants_count=2, entrant=entrant, entrants=[entrant])
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "1:42:06.9"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.racing_color

def test_timer_midrace_w_user_not_in_race():
    race = get_test_race(version=17, entrants_count=2, started_at=datetime.now(timezone.utc)-timedelta(hours=1, minutes=42, seconds=42.0))
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, "user_not_in_race#6969")
    assert color is None
    assert text == "1:42:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, "user_not_in_race#6969")
    assert color == timer.racing_color

def test_timer_race_cancelled():
    race = get_test_race(status_value="cancelled", cancelled_at=datetime.now(timezone.utc)+timedelta(minutes=20))
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, "")
    assert color is None
    assert text == "--:--:--.-"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, "")
    # currently, the timer is always red for canceled or dq races
    assert color is timer.cancel_dq_color

def test_timer_user_dqed():
    entrant = get_test_entrant(status_value="dq")
    race = get_test_race(entrant=entrant, entrants=[entrant])
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "--:--:--.-"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.cancel_dq_color

def test_user_finished_first():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, minutes=9, seconds=42, microseconds=1), place=1)
    race = get_test_race(started_at=datetime.now(timezone.utc)-entrant.finish_time, entrant=entrant, entrants_count=5, entrants=[entrant])
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "1:09:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.first_color

def test_user_finished_second():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, minutes=9, seconds=42, microseconds=1), place=2)
    race = get_test_race(started_at=datetime.now(timezone.utc)-entrant.finish_time, entrant=entrant, entrants_count=5, entrants=[entrant])
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "1:09:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.second_color

def test_user_finished_third():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, minutes=9, seconds=42, microseconds=1), place=3)
    race = get_test_race(started_at=datetime.now(timezone.utc)-entrant.finish_time, entrant=entrant, entrants_count=5, entrants=[entrant])
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "1:09:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.third_color

def test_user_finished_other():
    timer = get_test_timer()
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, minutes=9, seconds=42, microseconds=1), place=5)
    race = get_test_race(started_at=datetime.now(timezone.utc)-entrant.finish_time, entrant=entrant, entrants_count=5)
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "1:09:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.finished_color