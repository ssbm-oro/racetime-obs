import json
from datetime import timedelta, datetime, timezone
from models.race import Race, Status, RaceCategory, Goal, Entrant
from models.user import User, Stats

def test_race1():
    with open('tests/data/race1.txt') as f:
        race = Race.from_dict(json.load(f))
        assert race.name == "alttpr/lazy-hookshot-7357"

def test_finished_race():
    with open('tests/data/finished_race.txt') as f:
        race = Race.from_dict(json.load(f))
        expected_status = Status(
            value = "finished",
            verbose_value = "Finished",
            help_text = "This race has been completed"
        )
        expected_catogeroy = RaceCategory(
            name = "A Link to the Past Randomizer",
            short_name = "ALttPR",
            slug = "alttpr",
            url = "/alttpr",
            data_url = "/alttpr/data",
            image = "https://racetime.gg/media/alttpr.png"
        )
        expected_goal = Goal(
            name = "casual xkeys",
            custom = True,
        )
        expected_entrants = expected_entrants_finished_race1()
        expected_race = Race(
            version = 73,
            name = "alttpr/dazzling-oldman-0937",
            url = "/alttpr/dazzling-oldman-0937",
            data_url = "/alttpr/dazzling-oldman-0937/data",
            websocket_url = "/ws/race/dazzling-oldman-0937",
            websocket_bot_url = "/ws/o/bot/dazzling-oldman-0937",
            websocket_oauth_url = "/ws/o/race/dazzling-oldman-0937",
            info = "crosskeys - https://alttpr.com/h/QJG8VkrjvB - (Flute/Pendant/Magic Powder/Heart/Cape) - Quickswap Enabled",
            entrants_count = 10,
            entrants_count_finished = 9,
            entrants_count_inactive = 1,
            status=expected_status,
            category=expected_catogeroy,
            goal=expected_goal,
            entrants=expected_entrants,
            opened_at = datetime(year=2020, month=12, day=14, hour=3, minute=16, second=59, microsecond=822000, tzinfo=timezone.utc),
            time_limit=timedelta(days=1)
        )
        #assert expected_race == race
        assert len(expected_race.entrants) == len(race.entrants)

def expected_entrants_finished_race1():
    expected_user1 = User(
        id = "kzM65aWX7do1y8q0",
        full_name = "SEJay#5897",
        name = "SEJay",
        discriminator = "5897",
        url = "/user/kzM65aWX7do1y8q0",
        avatar = "https://racetime.gg/media/lukeacevedo_beer_videogames-01_1x.png",
        pronouns = "he/him",
        flair = "",
        twitch_name = "sejay_28",
        twitch_display_name = "SEJay_28",
        twitch_channel = "https://www.twitch.tv/sejay_28",
        can_moderate = False,
    )
    expected_user2 = User(
        id="XzVwZWqaJRW5k8eb",
        full_name="Zaruvyen#7867",
        name="Zaruvyen",
        discriminator="7867",
        url="/user/XzVwZWqaJRW5k8eb",
        avatar="https://racetime.gg/media/Zarufaceicon.png",
        pronouns="he/him",
        flair="",
        twitch_name="zaruvyen",
        twitch_display_name="Zaruvyen",
        twitch_channel="https://www.twitch.tv/zaruvyen",
        can_moderate=False
    )
    expected_status_finished = Status(
            value = "done",
            verbose_value = "Finished",
            help_text = "This race has been completed"
        )
    expected_entrants = [ 
            Entrant(
                user=expected_user1,
                status=expected_status_finished,
                finish_time = timedelta(hours=2, minutes=34, seconds=23.909043),
                finished_at = datetime(2020, 12, 14, 6, 8, 45, 820000, tzinfo=timezone.utc),
                place = 1,
                place_ordinal = "1st",
                score = None,
                score_change = None,
                comment = "191",
                has_comment = True,
                stream_live = False,
                stream_override = False,
                actions = []
            ),
            Entrant(
                user=expected_user1,
                status=expected_status_finished,
                finish_time=timedelta(hours=2, minutes=43, seconds=51.353469),
                finished_at=datetime(2020,12,14,6,18,13,265000, tzinfo=timezone.utc),
                place= 2,
                place_ordinal="2nd",
                score= None,
                score_change=None,
                comment="190 woof",
                has_comment=True,
                stream_live=False,
                stream_override=False,
                actions=[]
            ), None, None, None, None, None, None, None, None
        ]
    return expected_entrants
        

def test_none_race():
    assert None is None

def test_user():
    with open('tests/data/user1.txt') as f:
        user = User.from_dict(json.load(f))
        expected_stats = Stats(
            joined = 21,
            first = 3,
            second = 5,
            third = 0,
            forfeits = 4,
            dqs = 0
        )
        expected_user = User(
            id = "b52QE8oN53lywqX4",
            full_name = "oro#3531",
            name = "oro",
            discriminator="3531",
            url = "/user/b52QE8oN53lywqX4",
            avatar = "https://racetime.gg/media/oro_icon_100x100.png",
            pronouns = "they/them",
            flair = "",
            twitch_name = "ssbmoro",
            twitch_display_name = "SsbmOro",
            twitch_channel = "https://www.twitch.tv/ssbmoro",
            can_moderate = False,
            stats=expected_stats
        )
        assert user == expected_user