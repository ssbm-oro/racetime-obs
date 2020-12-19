from datetime import datetime, timedelta, timezone
from races_for_testing import time_ago
from gadgets.timer import Timer
from users_for_testing import get_test_entrant, get_test_entrants
from races_for_testing import get_test_race


def get_test_timer():
    timer = Timer()
    timer.source_name = "Timer source"
    timer.enabled = True
    return timer


def test_timer_prerace(random_users):
    timer = get_test_timer()
    race = get_test_race(
        status_value="open", version=12,
        started_at=None, start_delay=timedelta(seconds=-15),
        entrants=get_test_entrants(random_users)
    )
    color, text = timer.get_timer_text(race, "")
    assert color is None
    assert text == "-0:00:15.0"

    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, "")
    assert color is timer.pre_color
    assert text == "-0:00:15.0"


def test_timer_counting_down(random_users):
    timer = get_test_timer()
    race = get_test_race(
        status_value="pending", version=13, started_at=time_ago(seconds=-5),
        start_delay=timedelta(seconds=-15.0),
        entrants=get_test_entrants(random_users)
    )
    color, text = timer.get_timer_text(race, "")
    assert color is None
    assert text == "-0:00:05.0"

    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, "")
    assert color is timer.pre_color


def test_timer_midrace_no_entrant(random_users):
    timer = get_test_timer()
    race = get_test_race(
        status_value="in_progress", version=15, entrants_count=2,
        started_at=datetime.now(timezone.utc)-timedelta(hours=1, minutes=20),
        entrants=get_test_entrants(random_users)
    )
    color, text = timer.get_timer_text(race, "")
    assert color is None
    # hope this always runs in less than 0.1 seconds XD
    assert text == "1:20:00.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, "")
    assert color is timer.racing_color


def test_timer_midrace_w_entrant(random_users):
    entrant = get_test_entrant(
        next(random_users), status_value="finished",
        finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, minutes=42, seconds=6.9)
    )
    entrants = get_test_entrants(random_users, entrant)
    race = get_test_race(version=16, entrants=entrants)
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "1:42:06.9"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.racing_color


def test_timer_midrace_w_user_not_in_race(random_users):
    started_at = (
        datetime.now(timezone.utc) -
        timedelta(hours=1, minutes=42, seconds=42.0)
    )
    race = get_test_race(
        version=17, entrants=get_test_entrants(random_users),
        started_at=started_at
    )
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, "user_not_in_race#6969")
    assert color is None
    assert text == "1:42:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, "user_not_in_race#6969")
    assert color == timer.racing_color


def test_timer_race_cancelled(random_users):
    race = get_test_race(
        status_value="cancelled", entrants=get_test_entrants(random_users),
        cancelled_at=datetime.now(timezone.utc)+timedelta(minutes=20)
    )
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, "")
    assert color is None
    assert text == "--:--:--.-"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, "")
    # currently, the timer is always red for canceled or dq races
    assert color is timer.cancel_dq_color


def test_timer_user_dqed(random_users):
    entrant = get_test_entrant(next(random_users), status_value="dq")
    entrants = get_test_entrants(random_users, entrant)
    race = get_test_race(entrants=entrants)
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "--:--:--.-"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.cancel_dq_color


def test_user_finished_first(random_users):
    entrant = get_test_entrant(
        next(random_users), status_value="finished",
        finished_at=datetime.now(timezone.utc), place=1,
        finish_time=timedelta(hours=1, minutes=9, seconds=42, microseconds=1)
    )
    entrants = get_test_entrants(random_users, entrant)
    race = get_test_race(
        started_at=datetime.now(timezone.utc)-entrant.finish_time,
        entrants_count=5, entrants=entrants
    )
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "1:09:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.first_color


def test_user_finished_second(random_users):
    entrant = get_test_entrant(
        next(random_users), status_value="finished",
        finished_at=datetime.now(timezone.utc), place=2,
        finish_time=timedelta(hours=1, minutes=9, seconds=42, microseconds=1)
    )
    entrants = get_test_entrants(random_users, entrant)
    race = get_test_race(
        started_at=datetime.now(timezone.utc)-entrant.finish_time,
        entrants_count=5, entrants=entrants
    )
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "1:09:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.second_color


def test_user_finished_third(random_users):
    entrant = get_test_entrant(
        next(random_users), status_value="finished",
        finished_at=datetime.now(timezone.utc), place=3,
        finish_time=timedelta(hours=1, minutes=9, seconds=42, microseconds=1)
    )
    entrants = get_test_entrants(random_users, entrant)
    race = get_test_race(
        started_at=datetime.now(timezone.utc)-entrant.finish_time,
        entrants_count=5, entrants=entrants
    )
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "1:09:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.third_color


def test_user_finished_other(random_users):
    entrant = get_test_entrant(
        next(random_users), status_value="finished",
        finished_at=datetime.now(timezone.utc), place=5,
        finish_time=timedelta(hours=1, minutes=9, seconds=42, microseconds=1)
    )
    entrants = get_test_entrants(random_users, entrant)
    race = get_test_race(
        started_at=datetime.now(timezone.utc)-entrant.finish_time,
        entrants_count=5, entrants=entrants
    )
    timer = get_test_timer()
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color is None
    assert text == "1:09:42.0"
    timer.use_podium_colors = True
    color, text = timer.get_timer_text(race, entrant.user.full_name)
    assert color == timer.finished_color
