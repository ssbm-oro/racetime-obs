from datetime import datetime, time, timedelta, timezone
from gadgets.coop import Coop
from models.race import Entrant, Goal, Race, Status
from users_for_testing import get_test_user, get_test_entrant
from categories_for_testing import get_test_race_category
from races_for_testing import get_test_race

def test_coop_no_one_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(status_value="in_progress")
    opponent1 = get_test_entrant(status_value="in_progress")
    opponent2 = get_test_entrant(status_value="in_progress")

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == "Race still in progress"
    assert coop.text == " "

def test_only_entrant_finished():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    partner = get_test_entrant(status_value="in_progress")
    opponent1 = get_test_entrant(status_value="in_progress")
    opponent2 = get_test_entrant(status_value="in_progress")

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == "Race still in progress"
    assert coop.text == " "

def test_only_partner_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    opponent1 = get_test_entrant(status_value="in_progress")
    opponent2 = get_test_entrant(status_value="in_progress")

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == "Race still in progress"
    assert coop.text == " "

def test_only_opponent1_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(status_value="in_progress")
    opponent1 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    opponent2 = get_test_entrant(status_value="in_progress")

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == "Race still in progress"
    assert coop.text == " "

def test_only_opponent2_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(status_value="in_progress")
    opponent1 = get_test_entrant(status_value="in_progress")
    opponent2 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == "Race still in progress"
    assert coop.text == " "

def test_entrant_and_partner_finished():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    partner = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))
    opponent1 = get_test_entrant(status_value="in_progress")
    opponent2 = get_test_entrant(status_value="in_progress")

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == "We won!"
    assert coop.text == "1:30:00.0"

def test_opponents_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(status_value="in_progress")
    opponent1 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    opponent2 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == "They won. :("
    assert coop.text == "1:30:00.0"

def test_entrant_and_opponent1_finished():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))
    partner = get_test_entrant(status_value="in_progress")
    opponent1 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    opponent2 = get_test_entrant(status_value="in_progress")

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == "Race still in progress"
    assert coop.text == " "

def test_partner_and_opponent1_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))
    opponent1 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    opponent2 = get_test_entrant(status_value="in_progress")

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == "Race still in progress"
    assert coop.text == " "

def test_entrant_and_partner_and_opponent1_finished_race_ongoing():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    partner = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))
    opponent1 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    opponent2 = get_test_entrant(status_value="in_progress")

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == opponent2.user.name + " needs to finish before"
    assert coop.text == "2:00:00.0"

def test_entrant_and_partner_and_opponent1_finished_race_over():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    partner = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))
    opponent1 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=3, microseconds=2))
    opponent2 = get_test_entrant(status_value="in_progress")

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == f"{entrant.user.name} and {partner.user.name} won"
    assert coop.text == "1:30:00.0"

def test_opponents_and_entrant_finished_race_ongoing():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    partner = get_test_entrant(status_value="in_progress")
    opponent1 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=2))
    opponent2 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == f"{partner.user.name} needs to finish before"
    assert coop.text == "2:00:00.0"

def test_opponents_and_partner_finished_race_over():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=3, microseconds=3))
    opponent1 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    opponent2 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == f"{opponent1.user.name} and {opponent2.user.name} won"
    assert coop.text == "1:30:00.0"

def test_everyone_finished_we_won():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    partner = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))
    opponent1 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))
    opponent2 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == f"We won!!! Average time:"
    assert coop.text == "1:30:00.0"

def test_everyone_finished_opponents_won():
    entrant = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))
    partner = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))
    opponent1 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=1, microseconds=1))
    opponent2 = get_test_entrant(status_value="finished", finished_at=datetime.now(timezone.utc), finish_time=timedelta(hours=2, microseconds=1))

    race = get_test_race(entrants=[entrant, partner, opponent1, opponent2])
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.label_text == f"Opponents won, average time:"
    assert coop.text == "1:30:00.0"