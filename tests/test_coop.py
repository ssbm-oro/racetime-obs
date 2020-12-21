from datetime import datetime, timedelta, timezone

from gadgets.coop import Coop

from races_for_testing import get_test_race, time_ago
from users_for_testing import get_test_entrant


def test_coop_no_one_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(
        status_value="in_progress", users_used=[entrant.user.id]
        )
    opponent1 = get_test_entrant(
        status_value="in_progress",
        users_used=[
            entrant.user.id,
            partner.user.id
            ]
        )
    opponent2 = get_test_entrant(
        status_value="in_progress",
        users_used=[
            entrant.user.id,
            partner.user.id,
            opponent1.user.id
            ]
        )

    race = get_test_race(
        entrants=[
            entrant,
            partner,
            opponent1,
            opponent2
        ],
        started_at=time_ago(hours=1)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == " "
    assert coop.our_time_text == " "
    assert coop.our_time_color == coop.still_racing_color
    assert coop.opponent_time_color == coop.still_racing_color


def test_only_entrant_finished():
    entrant = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1)
    )
    partner = get_test_entrant(
        status_value="in_progress", users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="in_progress", users_used=[
            entrant.user.id, partner.user.id
        ]
    )
    opponent2 = get_test_entrant(
        status_value="in_progress", users_used=[
            entrant.user.id, partner.user.id, opponent1.user.id
        ]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=1, minutes=15)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == " "
    assert coop.our_time_text == " "
    assert coop.our_time_color == coop.still_racing_color
    assert coop.opponent_time_color == coop.still_racing_color


def test_only_partner_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1),
        users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="in_progress",
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="in_progress", users_used=[
                entrant.user.id, partner.user.id, opponent1.user.id
            ]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=1, minutes=15)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == " "
    assert coop.our_time_text == " "
    assert coop.our_time_color == coop.still_racing_color
    assert coop.opponent_time_color == coop.still_racing_color


def test_only_opponent1_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(
        status_value="in_progress", users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1),
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="in_progress",
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=1, minutes=15)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == " "
    assert coop.our_time_text == " "
    assert coop.our_time_color == coop.still_racing_color
    assert coop.opponent_time_color == coop.still_racing_color


def test_only_opponent2_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(
        status_value="in_progress", users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="in_progress",
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1),
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=1, minutes=15)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == " "
    assert coop.our_time_text == " "
    assert coop.our_time_color == coop.still_racing_color
    assert coop.opponent_time_color == coop.still_racing_color


def test_entrant_and_partner_finished():
    entrant = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1)
    )
    partner = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="in_progress",
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="in_progress",
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=2, minutes=15)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == "2:15:00.0"
    assert coop.our_time_text == "1:30:00.0"
    assert coop.our_time_color == coop.winner_color
    assert coop.opponent_time_color == coop.loser_color


def test_opponents_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(
        status_value="in_progress", users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1),
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=2, minutes=15)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == "1:30:00.0"
    assert coop.our_time_text == "2:15:00.0"
    assert coop.our_time_color == coop.loser_color
    assert coop.opponent_time_color == coop.winner_color


def test_entrant_and_opponent1_finished():
    entrant = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1)
    )
    partner = get_test_entrant(
        status_value="in_progress", users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1),
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="in_progress",
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=2, minutes=15)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == " "
    assert coop.our_time_text == " "
    assert coop.our_time_color == coop.still_racing_color
    assert coop.opponent_time_color == coop.still_racing_color


def test_partner_and_opponent1_finished():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1),
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="in_progress",
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=2, minutes=15)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == " "
    assert coop.our_time_text == " "
    assert coop.our_time_color == coop.still_racing_color
    assert coop.opponent_time_color == coop.still_racing_color


def test_entrant_and_partner_and_opponent1_finished_race_ongoing():
    entrant = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1)
    )
    partner = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1),
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="in_progress",
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=2, minutes=12)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == "0:23:59.9"
    assert coop.our_time_text == "2:00:00.0"
    assert coop.our_time_color == coop.still_racing_color
    assert coop.opponent_time_color == coop.still_racing_color
    race.started_at = time_ago(hours=2, minutes=52)
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == "0:03:59.9"


def test_entrant_and_partner_and_opponent1_finished_race_over():
    entrant = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1)
    )
    partner = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=3, microseconds=2),
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="in_progress",
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=3, minutes=4)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert (
        coop.opponent_time_text == "3:02:00.0"
    )
    assert coop.our_time_text == "1:30:00.0"


def test_opponents_and_entrant_finished_race_ongoing():
    entrant = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1)
    )
    partner = get_test_entrant(
        status_value="in_progress", users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=2),
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=2, microseconds=3)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == "2:00:00.0"
    assert coop.our_time_text == "0:29:59.9"
    race.started_at = time_ago(hours=2, minutes=30, microseconds=3)
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == "2:00:00.0"
    assert coop.our_time_text == "0:14:59.9"


def test_opponents_and_partner_finished_race_over():
    entrant = get_test_entrant(status_value="in_progress")
    partner = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=3, microseconds=5),
        users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1),
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=3, minutes=1)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)

    assert coop.opponent_time_text == "1:30:00.0"
    assert coop.opponent_time_color == coop.winner_color
    assert coop.our_time_text == "3:00:30.0"
    assert coop.our_time_color == coop.loser_color


def test_everyone_finished_we_won():
    entrant = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1)
    )
    partner = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=2, minutes=1)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == "2:00:00.0"
    assert coop.opponent_time_color == coop.loser_color
    assert coop.our_time_text == "1:30:00.0"
    assert coop.our_time_color == coop.winner_color


def test_everyone_finished_opponents_won():
    entrant = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1)
    )
    partner = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id]
    )
    opponent1 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=1, microseconds=1),
        users_used=[entrant.user.id, partner.user.id]
    )
    opponent2 = get_test_entrant(
        status_value="finished", finished_at=datetime.now(timezone.utc),
        finish_time=timedelta(hours=2, microseconds=1),
        users_used=[entrant.user.id, partner.user.id, opponent1.user.id]
    )

    race = get_test_race(
        entrants=[entrant, partner, opponent1, opponent2],
        started_at=time_ago(hours=2, minutes=1)
    )
    coop = Coop()
    coop.enabled = True
    coop.partner = partner.user.full_name
    coop.opponent1 = opponent1.user.full_name
    coop.opponent2 = opponent2.user.full_name
    coop.update_coop_text(race, entrant.user.full_name)
    assert coop.opponent_time_text == "1:30:00.0"
    assert coop.opponent_time_color == coop.winner_color
    assert coop.our_time_text == "2:00:00.0"
    assert coop.our_time_color == coop.loser_color
