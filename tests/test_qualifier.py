from datetime import timedelta
from gadgets.qualifier import Qualifier
from users_for_testing import get_test_entrant
from races_for_testing import get_test_race, time_ago


def get_test_qualifier():
    qualifier = Qualifier()
    qualifier.enabled = True
    qualifier.qualifier_cutoff = 3
    qualifier.par_source = "par source"
    qualifier.score_source = "score source"
    return qualifier


def test_no_one_finished():
    entrant = get_test_entrant(status_value="in_progress")
    race = get_test_race(entrants_count=20, entrant=entrant)
    qualifier = get_test_qualifier()
    qualifier.update_qualifier_text(race, entrant.user.full_name)
    assert qualifier.entrant_score == " "
    assert qualifier.par_text == " "


def test_some_finished():
    entrant = get_test_entrant(status_value="in_progress")
    first_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=20),
        finish_time=timedelta(hours=1, minutes=30, microseconds=1), place=1,
        users_used=[entrant.user.id]
    )
    second_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=15),
        finish_time=timedelta(hours=1, minutes=35, microseconds=1), place=2,
        users_used=[entrant.user.id, first_place.user.id]
    )
    entrants = [first_place, second_place, entrant]
    for i in range(3, 20):
        users_used = (x.user for x in entrants)
        entrants.append(get_test_entrant(users_used=users_used))
    race = get_test_race(entrants=entrants)
    qualifier = get_test_qualifier()
    qualifier.update_qualifier_text(race, entrant.user.full_name)
    assert qualifier.entrant_score == " "
    assert qualifier.par_text == " "


def test_cutoff_finished():
    entrant = get_test_entrant(status_value="in_progress")
    first_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=20),
        finish_time=timedelta(hours=1, minutes=30, microseconds=1), place=1,
        users_used=[entrant.user.id]
    )
    second_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=15),
        finish_time=timedelta(hours=1, minutes=35, microseconds=1), place=2,
        users_used=[entrant.user.id, first_place.user.id]
    )
    third_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=10),
        finish_time=timedelta(hours=1, minutes=40, microseconds=1), place=3,
        users_used=[entrant.user.id, first_place.user.id, second_place.user.id]
    )
    entrants = [first_place, second_place, third_place, entrant]
    for i in range(4, 20):
        users_used = (x.user for x in entrants)
        entrants.append(get_test_entrant(users_used=users_used))
    race = get_test_race(entrants=entrants)
    qualifier = get_test_qualifier()
    qualifier.update_qualifier_text(race, entrant.user.full_name)
    assert qualifier.entrant_score == " "
    assert qualifier.par_text == "1:35:00.0"


def test_cutoff_and_entrant_finished():
    entrant = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=5),
        finish_time=timedelta(hours=1, minutes=45, microseconds=1)
    )
    first_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=20),
        finish_time=timedelta(hours=1, minutes=30, microseconds=1), place=1,
        users_used=[entrant.user.id]
    )
    second_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=15),
        finish_time=timedelta(hours=1, minutes=35, microseconds=1), place=2,
        users_used=[entrant.user.id, first_place.user.id]
    )
    third_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=10),
        finish_time=timedelta(hours=1, minutes=40, microseconds=1), place=3,
        users_used=[entrant.user.id, first_place.user.id, second_place.user.id]
    )
    entrants = [first_place, second_place, third_place, entrant]
    for i in range(4, 20):
        users_used = (x.user for x in entrants)
        entrants.append(get_test_entrant(users_used=users_used))
    race = get_test_race(entrants=entrants)
    qualifier = get_test_qualifier()
    qualifier.update_qualifier_text(race, entrant.user.full_name)
    # par is 95 minutes, entrant's time is 105 minutes. 2-(105/95) ~= 0.89
    assert qualifier.entrant_score == "0.89"
    assert qualifier.par_text == "1:35:00.0"


def test_cutoff_and_entrant_finished_in_top():
    entrant = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=15),
        finish_time=timedelta(hours=1, minutes=35, microseconds=1), place=2
    )
    first_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=20),
        finish_time=timedelta(hours=1, minutes=30, microseconds=1), place=1,
        users_used=[entrant.user.id]
    )
    third_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=10),
        finish_time=timedelta(hours=1, minutes=40, microseconds=1), place=3,
        users_used=[entrant.user.id, first_place.user.id]
    )
    entrants = [first_place, entrant, third_place]
    for i in range(4, 20):
        users_used = (x.user for x in entrants)
        entrants.append(get_test_entrant(users_used=users_used))
    race = get_test_race(entrants=entrants)
    qualifier = get_test_qualifier()
    qualifier.update_qualifier_text(race, entrant.user.full_name)
    # par is 95 minutes, entrant's time is 95 minutes. 2-(95/95) = 1.00
    assert qualifier.entrant_score == "1.00"
    assert qualifier.par_text == "1:35:00.0"


def test_cutoff_and_entrant_finished_in_first():
    entrant = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=20),
        finish_time=timedelta(hours=1, minutes=30, microseconds=1), place=2
    )
    second_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=15),
        finish_time=timedelta(hours=1, minutes=35, microseconds=1), place=1,
        users_used=[entrant.user.id]
    )
    third_place = get_test_entrant(
        status_value="finished", finished_at=time_ago(minutes=10),
        finish_time=timedelta(hours=1, minutes=40, microseconds=1), place=3,
        users_used=[entrant.user.id, second_place.user.id]
    )
    entrants = [entrant, second_place, third_place]
    for i in range(4, 20):
        users_used = (x.user for x in entrants)
        entrants.append(get_test_entrant(users_used=users_used))
    race = get_test_race(entrants=entrants)
    qualifier = get_test_qualifier()
    qualifier.update_qualifier_text(race, entrant.user.full_name)
    # par is 95 minutes, entrant's time is 90 minutes. 2-(90/95) ""= 1.05
    assert qualifier.entrant_score == "1.05"
    assert qualifier.par_text == "1:35:00.0"
